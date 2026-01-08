import sys
import os
import random
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from keybert import KeyBERT

app = FastAPI()

# --- Path Magic to import from root ---
# We need to import 'model.predict' which is at the project root level (relative to this service).
# But 'model.predict' assumes CWD is project root to load "model/bert_fakenews".
# So we temporarily switch CWD to project root for the import.

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

original_cwd = os.getcwd()
try:
    os.chdir(project_root)
    # Check if model/predict.py exists or if it's just predict.py
    if os.path.exists(os.path.join(project_root, "model", "predict.py")):
        from model.predict import predict_news, tokenizer
    elif os.path.exists(os.path.join(project_root, "predict.py")):
        from predict import predict_news, tokenizer
    else:
        # Fallback for robustness, though we expect it in model/predict.py based on checks
        raise ImportError("Could not find predict.py in model/ or root")

    # Import scrapers
    from scrapers.google_news_scraper import fetch_google_news
    from scrapers.reddit_scraper import fetch_reddit_posts

except ImportError as e:
    # If dependencies are missing in the env, this will fail.
    print(f"Error importing model or scrapers: {e}")
    # Define dummy placeholders so app can at least start (though endpoint will fail)
    def predict_news(text): raise NotImplementedError("Model not loaded")
    def fetch_google_news(query, max_results=5): return []
    def fetch_reddit_posts(query, limit=5): return []
    tokenizer = None
finally:
    # Restore CWD so we don't confuse other things if needed
    os.chdir(original_cwd)

# --- Init KeyBERT ---
try:
    kw_model = KeyBERT()
except Exception as e:
    print(f"Warning: KeyBERT failed to initialize: {e}")
    kw_model = None

def build_search_term(text: str) -> str:
    if not kw_model:
        return text
    
    words = text.split()
    if len(words) <= 12:
        return text 

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=3,
    )
    keyphrases = [kw for kw, _ in keywords if len(kw.split()) > 1]
    if not keyphrases:
        keyphrases = [kw for kw, _ in keywords]

    return " ".join(keyphrases)

# --- Pydantic Models ---

class PredictRequest(BaseModel):
    text: str

class Highlight(BaseModel):
    span: str
    score: float

class Explanation(BaseModel):
    summary: str
    method: str
    highlights: List[Highlight]

class SocialPost(BaseModel):
    text: str
    url: str
    source: str # 'reddit' or 'google'
    published: Optional[str] = None

class PredictResponse(BaseModel):
    label: str
    confidence: float
    probs: List[float]
    explanation: Explanation
    social_context: List[SocialPost]

# --- Logic ---

@app.post("/predict_explain", response_model=PredictResponse)
def predict_explain_endpoint(request: PredictRequest):
    text = request.text
    
    # 1. Get Prediction
    try:
        label, confidence, probs = predict_news(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")

    # 2. Generate Explanation (MVP Heuristic)
    # "Pick top 8 tokens by a simple heuristic (e.g., longer alphabetic tokens, excluding stopwords/punctuation)."
    
    if tokenizer:
        tokens = tokenizer.tokenize(text)
    else:
        tokens = text.split() # Fallback

    # Filter candidates: alphabetic and len > 3 is a decent proxy for "content words"
    # We also want to map them back to the text or just return the tokens as spans.
    # The requirement says "span": "<token_or_phrase>"
    
    candidates = []
    seen = set()
    for t in tokens:
        # Clean up token (BERT tokens often start with ##)
        clean_t = t.replace("##", "")
        if clean_t.isalpha() and len(clean_t) > 3 and clean_t.lower() not in seen:
            candidates.append(clean_t)
            seen.add(clean_t.lower())
    
    # Sort by length (heuristic: longer words are more specific?) or just take first 8?
    # "Pick top 8 tokens by a simple heuristic" -> Let's sort by length descending.
    candidates.sort(key=len, reverse=True)
    top_tokens = candidates[:8]
    
    highlights = []
    for token_str in top_tokens:
        # Score: min(1.0, confidence + small jitter based on token length)
        # Jitter: len(token) * 0.01
        jitter = len(token_str) * 0.01
        score = min(1.0, confidence + jitter)
        highlights.append(Highlight(span=token_str, score=score))

    summary_text = f"The model predicts this is {label} with {confidence:.2f} confidence."

    explanation = Explanation(
        summary=summary_text,
        method="simple_rationale_v1",
        highlights=highlights
    )

    # 3. Fetch Social Context (only if REAL, per app.py logic)
    social_context = []
    if label.upper() != "FAKE":
        try:
            search_term = build_search_term(text)
            
            # Fetch Reddit
            r_posts = fetch_reddit_posts(search_term, limit=5)
            for p in r_posts:
                social_context.append(SocialPost(
                    text=p['text'],
                    url=p['url'],
                    source='reddit'
                ))
            
            # Fetch Google News
            g_posts = fetch_google_news(search_term, max_results=5)
            for p in g_posts:
                social_context.append(SocialPost(
                    text=p['text'],
                    url=p['url'],
                    source='google',
                    published=p.get('published')
                ))
                
        except Exception as e:
            print(f"Error fetching social context: {e}")
            # Continue without context rather than failing the whole request

    return PredictResponse(
        label=label,
        confidence=confidence,
        probs=probs,
        explanation=explanation,
        social_context=social_context
    )

@app.get("/health")
def health():
    return {"status": "ok"}

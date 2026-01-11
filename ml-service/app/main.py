import sys
import os
import random
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from keybert import KeyBERT

# Import from our new model loader
from app.model_loader import predict_news, get_tokenizer

app = FastAPI()

# --- Path Magic for Scrapers ---
# We still need scrapers from the root project.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

# Import scrapers
try:
    from scrapers.google_news_scraper import fetch_google_news
    from scrapers.reddit_scraper import fetch_reddit_posts
except ImportError as e:
    print(f"Error importing scrapers: {e}")
    def fetch_google_news(query, max_results=5): return []
    def fetch_reddit_posts(query, limit=5): return []

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
        # This will trigger download/load on first request
        label, confidence, probs = predict_news(text)
    except Exception as e:
        print(f"Prediction failed: {e}")
        # If the model fails to load/download, return 503 as requested
        raise HTTPException(status_code=503, detail="Model unavailable or failed to load.")

    # 2. Generate Explanation (MVP Heuristic)
    tokenizer = None
    try:
        tokenizer = get_tokenizer()
    except:
        pass # Should be loaded if predict_news succeeded

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
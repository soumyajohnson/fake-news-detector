import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download

# Configuration
REPO_ID = os.getenv("HF_REPO_ID", "SoumyaJohnson/bert_fakenews")
MODEL_FILENAME = os.getenv("HF_MODEL_FILE", "model.safetensors")
CONFIG_FILENAME = "config.json"
VOCAB_FILENAME = "vocab.txt"

# Cache Path
def get_hf_home():
    if os.path.exists("/var/data"):
        return "/var/data/huggingface"
    return "/tmp/huggingface"

HF_HOME = os.getenv("HF_HOME", get_hf_home())
# Ensure the directory exists
os.makedirs(HF_HOME, exist_ok=True)
# Set the env var for other HF tools if they use it implicitly
os.environ["HF_HOME"] = HF_HOME

_model = None
_tokenizer = None
LABELS = {0: "FAKE", 1: "REAL"}

def load_model():
    global _model, _tokenizer
    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    print(f"Loading model from {REPO_ID} into {HF_HOME}...")
    try:
        # Download files
        # We explicitly download model.safetensors as requested
        model_path = hf_hub_download(repo_id=REPO_ID, filename=MODEL_FILENAME, cache_dir=HF_HOME)
        # Download auxiliary files needed for instantiation
        hf_hub_download(repo_id=REPO_ID, filename=CONFIG_FILENAME, cache_dir=HF_HOME)
        hf_hub_download(repo_id=REPO_ID, filename=VOCAB_FILENAME, cache_dir=HF_HOME)
        
        # Use the directory of the downloaded files to load the model
        model_dir = os.path.dirname(model_path)
        
        _tokenizer = AutoTokenizer.from_pretrained(model_dir)
        _model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        _model.eval()
        
        print("Model loaded successfully.")
        return _model, _tokenizer
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

def predict_news(text: str):
    try:
        model, tokenizer = load_model()
    except Exception as e:
        # If model loading fails, we should probably let it bubble up or handle it.
        # The prompt says: "handle download failures gracefully (clear error logs + return a 503)"
        # We'll catch this in the FastAPI endpoint.
        raise e
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)[0]

    pred_class = torch.argmax(probs).item()
    confidence = probs[pred_class].item()

    label = LABELS[pred_class]

    return label, confidence, probs.tolist()

def get_tokenizer():
    _, tokenizer = load_model()
    return tokenizer

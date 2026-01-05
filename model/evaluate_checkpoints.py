import os
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, f1_score

# ====== CONFIG ======
CHECKPOINT_ROOT = "model_output"
TEST_CSV_PATH   = "data/manual_test.csv"
TEXT_COL        = "text"
LABEL_COL       = "label"
BASE_MODEL      = "distilbert-base-uncased"   # tokenizer source
# ====================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {device}")

# Load test dataset
df = pd.read_csv(TEST_CSV_PATH)
texts = df[TEXT_COL].astype(str).tolist()
labels = df[LABEL_COL].tolist()
print(f"[INFO] Loaded {len(df)} test samples")

# Find checkpoints
checkpoints = []
for name in os.listdir(CHECKPOINT_ROOT):
    if name.startswith("checkpoint-"):
        step = int(name.split("-")[-1])
        checkpoints.append((step, os.path.join(CHECKPOINT_ROOT, name)))

checkpoints = sorted(checkpoints)
print("[INFO] Found checkpoints:")
for step, path in checkpoints:
    print(f"  - {path} (step {step})")

# Load tokenizer from base model (NOT checkpoint)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

results = []

for step, ckpt_path in checkpoints:
    print(f"\n[INFO] Evaluating {ckpt_path} ...")

    model = AutoModelForSequenceClassification.from_pretrained(ckpt_path)
    model.to(device)
    model.eval()

    preds = []

    with torch.no_grad():
        for text in texts:
            enc = tokenizer(text, return_tensors="pt", truncation=True).to(device)
            out = model(**enc)
            pred = torch.argmax(out.logits).item()
            preds.append(pred)

    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average="weighted")

    print(f"[RESULT] step {step}: acc={acc:.4f}, f1={f1:.4f}")
    results.append((step, acc, f1))

print("\n=== SUMMARY ===")
for step, acc, f1 in results:
    print(f"step {step}: acc={acc:.4f}, f1={f1:.4f}")

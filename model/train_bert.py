import os
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)

# === 1. Load and label dataset ===
base_path = "C:/Users/soumy/fake-news-detector/data"
files = {
    "politifact_real.csv": 1,
    "politifact_fake.csv": 0,
    "gossipcop_real.csv": 1,
    "gossipcop_fake.csv": 0
}

all_data = []
for file_name, label in files.items():
    path = os.path.join(base_path, file_name)
    df = pd.read_csv(path)
    if "title" in df.columns:
        df = df[["title"]]
        df["label"] = label
        all_data.append(df)

df_full = pd.concat(all_data).dropna().reset_index(drop=True)

# === 2. Split into train and validation sets ===
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df_full["title"].tolist(), df_full["label"].tolist(), test_size=0.2, random_state=42
)

# === 3. Tokenize the texts ===
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

# === 4. PyTorch Dataset class ===
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        return {
            **{key: torch.tensor(val[idx]) for key, val in self.encodings.items()},
            "labels": torch.tensor(self.labels[idx])
        }

train_dataset = NewsDataset(train_encodings, train_labels)
val_dataset = NewsDataset(val_encodings, val_labels)

# === 5. Load model ===
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# === 6. Define custom weighted loss function ===
class_weights = torch.tensor([3.0, 1.0])  # More weight on class 0 (FAKE)P
loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights.to(model.device))

# def compute_loss(model, inputs, return_outputs=False, **kwargs):
#     # Hugging Face Trainer passes a dict-like object with keys like input_ids, attention_mask, labels
#     if isinstance(inputs, dict):
#         labels = inputs["labels"]
#         input_data = {k: v for k, v in inputs.items() if k != "labels"}
#     else:
#         raise TypeError("Expected inputs to be a dictionary")

#     outputs = model(**input_data)
#     logits = outputs.logits

#     class_weights = torch.tensor([3.0, 1.0]).to(logits.device)
#     loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights)
#     loss = loss_fn(logits, labels)

#     return (loss, outputs) if return_outputs else loss

# === 7. Training Arguments ===
training_args = TrainingArguments(
    output_dir="./model_output",
    eval_strategy="epoch",             # Evaluate at the end of each epoch
    save_strategy="epoch",                   # Save model at each epoch
    logging_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    weight_decay=0.01,
    logging_dir="./logs",
)

from transformers import Trainer

class WeightedLossTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs["labels"]
        inputs = {k: v for k, v in inputs.items() if k != "labels"}

        outputs = model(**inputs)
        logits = outputs.logits

        # Class weight: more importance to FAKE (class 0)
        class_weights = torch.tensor([3.0, 1.0]).to(logits.device)
        loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights)

        loss = loss_fn(logits, labels)
        return (loss, outputs) if return_outputs else loss

# === 8. Trainer ===
trainer = WeightedLossTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    #compute_loss_func=compute_loss  # Custom loss function
)

# === 9. Train ===
trainer.train()

# === 10. Evaluate ===
preds = trainer.predict(val_dataset)
y_pred = preds.predictions.argmax(-1)
print(classification_report(val_labels, y_pred))

# === 11. Save model and tokenizer ===
model.save_pretrained("./model/bert_fakenews")
tokenizer.save_pretrained("./model/bert_fakenews")

print("✅ DistilBERT model with class weighting fine-tuned and saved!")

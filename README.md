# 📰 AI-Driven Fake News Detection System

This repository contains an AI-based fake news detection system built using modern
Natural Language Processing (NLP) techniques. The project uses transformer-based
models (BERT) to classify news articles or headlines as **real** or **fake**, and is
designed to be modular, reproducible, and easy to deploy as a web application.

To keep the repository lightweight and GitHub-friendly, datasets and trained model
weights are not committed and are instead referenced externally.

---

## 🚀 Features
- Fake news classification using BERT-based NLP models
- Modular training, evaluation, and inference scripts
- Flask-based web application for interactive predictions
- Checkpoint evaluation and accuracy analysis utilities
- Clean separation of data, model logic, and UI templates

---

## 📊 Dataset

The dataset is **not included** in this repository.

You may use publicly available fake news datasets such as:
- **FakeNewsNet** (PolitiFact + GossipCop)
- Kaggle Fake News datasets
- Custom scraped news articles

After downloading, place the dataset files inside the `data/` directory.

---

## 📥 Model Weights (Hosted on Hugging Face)

Trained model weights are hosted externally on **Hugging Face**.

### Download Link
[Download model.safetensor](https://huggingface.co)

### Automatic Download in Python

The model can be downloaded automatically at runtime using the Hugging Face Hub:

```python
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="your-username/my-awesome-model",
    filename="model.safetensor"
)

print(f"Model downloaded to: {model_path}")



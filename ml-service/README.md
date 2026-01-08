# ML Service

This is the Python FastAPI service for the Fake News Detector. It loads the trained BERT model and serves predictions.

## Setup & Run

It is recommended to run this service from the `ml-service` directory.

1.  **Navigate to directory:**
    ```bash
    cd ml-service
    ```

2.  **Create Virtual Environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate Virtual Environment:**
    - Windows: `.venv\Scripts\activate`
    - Linux/Mac: `source .venv/bin/activate`

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run Service:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

## API Usage

**Endpoint:** `POST /predict_explain`

### Test Commands (Curl)

**1. Real News Example:**
```bash
curl -X POST "http://localhost:8000/predict_explain" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"Scientists verify that the earth is indeed round based on satellite imagery and physics.\"}"
```

**2. Fake News Example:**
```bash
curl -X POST "http://localhost:8000/predict_explain" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"Aliens have taken over the government and are replacing water with soda!\"}"
```

**3. Short Text:**
```bash
curl -X POST "http://localhost:8000/predict_explain" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"Breaking news: nothing happened today.\"}"
```

# Fake News Detector - Mono-repo Architecture

This project has been expanded to a mono-repo structure containing a Python ML service and a Java Spring Boot backend.

## Architecture

- **ml-service**: A Python FastAPI service that hosts the Machine Learning model. It exposes endpoints to predict whether a news text is fake or real and provides an explanation.
- **java-backend**: A Spring Boot application that acts as the main backend gateway. It handles user requests and communicates with the `ml-service` for predictions.

## Prerequisites

- Python 3.9+
- Java 17+
- Maven
- Docker (optional)

## How to Run

### ML Service (Python)

1. Navigate to `ml-service/`:
   ```bash
   cd ml-service
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the service:
   ```bash
   uvicorn main:app --reload
   ```
   The service will be available at `http://localhost:8000`.

### Java Backend (Spring Boot)

1. Navigate to `java-backend/`:
   ```bash
   cd java-backend
   ```
2. Build and run the application:
   ```bash
   mvn spring-boot:run
   ```
   The application will be available at `http://localhost:8080`.

## API Endpoints

### ML Service
- `POST /predict_explain`: Accepts JSON `{ "text": "news content" }`. Returns prediction and explanation.

### Java Backend
- `GET /api/check?text=...`: Checks the news text. (Currently a placeholder that returns a status message).




How to Run

   1. Start the ML Service (must be running for the Java backend to work fully):

   1     cd ml-service
   2     uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

   2. Start the Java Backend:

   1     cd java-backend
   2     mvn spring-boot:run

  Test Command (Curl)

   1 curl -X POST "http://localhost:8080/api/check" \
   2      -H "Content-Type: application/json" \
   3      -d "{\"text\": \"This is a test news article to check if the system works.\"}"


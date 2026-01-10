# AI-Powered Fake News Detector

A full-stack web application for analyzing news credibility using natural language processing (NLP) and real-time social context enrichment.

## Problem Statement

The rapid spread of misinformation poses significant challenges to public trust and decision-making. Simple binary classifiers often fail to provide sufficient context or transparency, leaving users uncertain about *why* a piece of content is flagged. This system addresses this gap by combining deep learning-based text analysis with explainable AI (XAI) and real-time social signals (Google News, Reddit) to provide a comprehensive credibility assessment.

## System Overview

This project implements a modular, microservices-style architecture designed for scalability and clear separation of concerns:

-   **Frontend (Angular):** A responsive single-page application (SPA) handling user interaction, authentication, and data visualization.
-   **Backend API (Spring Boot):** The central orchestrator managing user sessions, business logic, data persistence, and communication with the ML service.
-   **ML Service (Python):** A dedicated service responsible for NLP inference, explanation generation, and external social media scraping.

Communication between services is handled via RESTful APIs, ensuring statelessness and flexibility.

## Key Features

-   **Secure Authentication:** User registration and login using JWT (JSON Web Tokens).
-   **Credibility Analysis:** Real-time prediction of "Real" vs. "Fake" news with confidence scores.
-   **Explainable AI:** Provides natural language explanations and key indicator highlights for model decisions.
-   **Social Context:** Automatically retrieves related discussions from Reddit and Google News to provide external verification.
-   **History Management:** Users can save, search, filter, and delete their past analysis history.
-   **Modern UI:** A clean, responsive interface built with Angular Material and custom SCSS.

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Angular, TypeScript, SCSS, Angular Material |
| **Backend** | Java, Spring Boot, Spring Security |
| **ML Service** | Python, FastAPI/Flask (implied), NLP Libraries (Transformers/Scikit-learn) |
| **Authentication** | JWT (Stateless) |
| **Communication** | REST API (JSON) |
| **Persistence** | MongoDB (Document Store) |

## Frontend Architecture

The frontend is a component-based Angular application designed for maintainability and performance.

-   **Authentication Flow:** Login and Register pages route to a secure dashboard upon success. Auth guards protect sensitive routes (`/check`, `/history`).
-   **Dashboard:** The core analysis interface allows users to input text/URLs and view results immediately.
-   **Visualization:** Results are presented as a structured report, featuring confidence bars, pill-based status indicators, and organized lists for social context.
-   **State Management:** Services (`AuthService`, `NewsService`) manage API communication and local state using RxJS observables.

## Backend Architecture

The Spring Boot backend serves as the secure gateway for the application.

-   **Controller Layer:** Exposes REST endpoints for Auth, News Checks, and History.
-   **Service Layer:** Encapsulates business logic, including user validation and ML service orchestration.
-   **Security Configuration:** Implements a `JwtAuthenticationFilter` to validate tokens on every protected request.
-   **Integration:** Proxies analysis requests to the Python ML service to decouple the heavy lifting from the web server.

## ML Service Architecture

The Python service acts as the intelligence engine.

-   **NLP Pipeline:** Preprocesses text inputs (tokenization, cleaning) before passing them to the model.
-   **Classification:** Utilizes a trained NLP model (e.g., DistilBERT/RoBERTa fine-tuned on fake news datasets) to generate predictions.
-   **Explainability:** Generates human-readable rationales for the model's output.
-   **Scrapers:** Modules for `google_news_scraper`, `reddit_scraper`, etc., fetch live context to augment the static analysis.

## Setup Instructions

### Prerequisites
-   Node.js & npm (Frontend)
-   Java JDK 17+ & Maven (Backend)
-   Python 3.8+ (ML Service)
-   MongoDB (Running locally or cloud URI)

### 1. Frontend Setup
```bash
cd fake-news-frontend
npm install
npm start
# Access at http://localhost:4200
```

### 2. Backend Setup
```bash
cd java-backend
# Update application.properties with your DB URI and JWT Secret
mvn clean install
mvn spring-boot:run
# API runs at http://localhost:8080
```

### 3. ML Service Setup
```bash
cd ml-service
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app/main.py
# Service runs at http://localhost:8000
```

## API Endpoints (High Level)

### Authentication
-   `POST /api/auth/register` - Create a new user account.
-   `POST /api/auth/login` - Authenticate and receive a JWT.

### News Analysis
-   `POST /api/check` - Submit text/URL for analysis. Returns prediction + explanation + social context.

### User History
-   `GET /api/history` - Retrieve all past checks for the logged-in user.
-   `GET /api/history/{id}` - Get detailed report for a specific check.
-   `DELETE /api/history/{id}` - Remove a specific record.

## Security Considerations

-   **Stateless Auth:** No sessions are stored on the server; the JWT contains all necessary claims.
-   **Route Protection:** Angular AuthGuards prevent unauthorized client-side navigation.
-   **Input Validation:** Backend uses Jakarta Validation constraints to sanitize inputs.
-   **Password Hashing:** Passwords are encrypted before storage (BCrypt).

## Future Improvements

-   **Model Versioning:** Dynamic loading of updated model weights without downtime.
-   **Source Reputation:** Integrating a "domain credibility" score based on known verified sources.
-   **Browser Extension:** A lightweight extension to check news directly on social media feeds.
-   **Monitoring:** Prometheus/Grafana integration for API latency and model drift monitoring.

## Screenshots

*(Placeholders for UI Screenshots: Dashboard, Analysis Result, History View)*

![Dashboard Placeholder](#)
![Analysis Report Placeholder](#)

## Author & Purpose

This project demonstrates the design and implementation of a production-ready, full-stack machine learning application. It highlights skills in system architecture, microservices integration, and secure web development standards suitable for enterprise environments.

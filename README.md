# 🌾 KrishiMitra Backend

## 🌟 Overview

KrishiMitra is a comprehensive AI-powered platform designed to assist farmers with modern, data-driven agricultural practices. This repository contains the **FastAPI backend** that powers the application, providing various services ranging from AI-driven crop recommendations and disease detection to real-time market prices, weather updates, and a community forum.

The application is built using **FastAPI** for high performance and **MongoDB** (via Motor) for flexible data storage.

## ✨ Features

The backend exposes a robust set of API endpoints to support farmer needs:

| Feature Area | Description | Endpoints (Examples) |
| :--- | :--- | :--- |
| **Authentication** | Secure user registration and login using JWT. | `/auth/signup`, `/auth/login` |
| **AI Assistant** | Interactive chat with KrishiMitra (GPT-4o-mini) for farming advice. | `/assistant/ask` |
| **Market Data** | Real-time commodity market prices fetched from external APIs. | `/market/market-price/{crop_name}` |
| **Geospatial Data** | Fetch detailed soil composition data (e.g., pH, texture) using coordinates via SoilGrids. | `/soil/soil?lat=...&lon=...` |
| **Weather** | Current weather conditions for any given city via OpenWeatherMap. | `/weather/weather/{city}` |
| **Community** | Forum for farmers to post questions and reply to peers. | `/community/post`, `/community/reply/{post_id}` |
| **Recommendations** | Mocked (to be replaced with ML) endpoints for Crop Recommendations and Disease Detection. | `/crop/recommend`, `/disease/detect` |
| **Govt. Schemes** | Fetch and sync relevant government schemes for farmers. | `/schemes/all`, `/schemes/sync` |
| **Farmer Profile** | CRUD operations for managing farmer-specific profile data. | `/farmer/create`, `/farmer/me`, `/farmer/update` |

## 🛠️ Tech Stack

  * **Framework:** FastAPI (Python)
  * **Database:** MongoDB (Asynchronous connectivity via `Motor`)
  * **Authentication:** JWT (JSON Web Tokens) with `passlib` (Bcrypt)
  * **External APIs:** OpenAI (AI Assistant), OpenWeatherMap, Data.gov.in (Market Price), ISRIC SoilGrids (Soil Data)
  * **Environment Management:** `python-dotenv`

## 🚀 Setup and Installation

### Prerequisites

  * Python 3.10+
  * MongoDB instance (local or remote)
  * API keys for external services (OpenAI, OpenWeatherMap, Data.gov.in, SoilGrids)

### 1\. Clone the repository

```bash
git clone <your-repository-url>
cd krishimitra-backend
```

### 2\. Set up the virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
```

### 3\. Install dependencies

```bash
pip install -r requirements.txt
# Note: requirements.txt is not provided, but based on the code, you'll need:
# fastapi, uvicorn, motor, python-dotenv, passlib[bcrypt], python-jose[cryptography], openai, httpx, beautifulsoup4, pydantic
```

### 4\. Configure Environment Variables

Create a file named **`.env`** in the root directory and populate it with your keys and configuration:

```ini
# Database
MONGO_URL="mongodb://localhost:27017/krishimitra"

# Security
JWT_SECRET="supersecurejwtsecretkey"
JWT_ALGORITHM="HS256"

# External APIs
OPENAI_API_KEY="sk-..."
OPENWEATHER_API_KEY="<your_open_weather_api_key>"
MARKET_API_KEY="<your_data_gov_in_api_key>"
SOILGRIDS_BASE_URL="https://rest.isric.org/soilgrids/v2.0/properties/query"
```

### 5\. Run the Application

The application is typically run using `uvicorn`.

```bash
uvicorn app.Main:app --reload
```

The server will start running at `http://127.0.0.1:8000`.

## 📖 API Documentation

Once the server is running, you can access the **Swagger UI** for interactive documentation and testing of all endpoints:

👉 **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**

## 📂 Project Structure

The project is logically organized using FastAPI's `APIRouter` system, with services separated into distinct modules:

```
KRISHIMITRA/
├── app/
│   ├── routers/                 # API Route handlers (Endpoints)
│   │   ├── assistant.py         # AI/Chatbot assistant logic
│   │   ├── auth.py              # User authentication & JWT handling
│   │   ├── community.py         # Community forum & social features
│   │   ├── crop.py              # Crop management & recommendation endpoints
│   │   ├── disease.py           # Plant disease detection & remedies
│   │   ├── farmer.py            # Farmer profile & user management
│   │   ├── market.py            # Real-time market price (Mandi) APIs
│   │   ├── schemes.py           # Government schemes retrieval
│   │   ├── soil.py              # Soil health analysis & reporting
│   │   └── weather.py           # Weather forecasting & alerts
│   ├── services/                # Business logic & background tasks
│   │   ├── crud.py              # Reusable CRUD database operations
│   │   └── schemes_sync.py      # Sync service for external scheme data
│   ├── db.py                    # Database connection & session management
│   └── main.py                  # Application entry point & configuration
├── .env                         # Environment variables (API keys, DB URL)
├── .gitignore                   # Git ignore rules
└── requirements.txt             # Python dependencies
```

## 🤝 Contributing

We welcome contributions\! If you have suggestions for new features (especially ML model integration for `crop.py` and `disease.py`), improvements, or bug fixes, please open an issue or submit a pull request.

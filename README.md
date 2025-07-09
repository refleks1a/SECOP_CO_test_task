    # Real-time Coin Data Tracking System

## Endpoints

- `POST /register` – Register a new user
- `POST /login` – Obtain a JWT token
- `GET /me` – Get user info (requires token)
- `ws/coin-track` – WebSocket for real-time coin price tracking

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

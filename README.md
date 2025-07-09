    # Real-time Coin Data Tracking System

This project is a FastAPI-based backend for real-time cryptocurrency price tracking using the CoinGecko API. Users can register, log in, and track coin prices via WebSocket.

## Features

- User registration and login (JWT-based authentication)
- Real-time coin price tracking via WebSocket
- Fetches prices from CoinGecko API

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

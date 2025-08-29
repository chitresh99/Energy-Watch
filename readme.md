# Energy Watch

Energy Watch is a FastAPI-based application that fetches and stores stock data for major energy companies using the [FinancialData.net](https://financialdata.net/) API and PostgreSQL (Neon DB).

## Features

- Fetch stock data for a list of energy companies via POST `/stocksall` endpoint.
- Retrieve latest stock data for a specific symbol via GET `/stocks/{symbol}` endpoint.
- Stores historical stock prices in PostgreSQL (Neon DB).

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL (Neon DB)
- **API:** [FinancialData.net](https://financialdata.net/)
- **ORM:** SQLAlchemy
- **HTTP Client:** httpx
- **Environment Variables:** python-dotenv

## Setup

1. Clone the repository:

```bash
git clone git@github.com:chitresh99/Energy-Watch.git
cd energy-watch
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

API Endpoints

POST /stocksall
Fetch and store all stock data for predefined energy companies.

GET /stocks/{symbol}
Retrieve the latest stock data for a specific company symbol.

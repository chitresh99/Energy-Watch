from fastapi import FastAPI, Depends
import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, get_db
import models
import json

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("FINANCIAL_DATA_API_KEY")
BASE_URL = os.getenv("BASE_URL")
stocklist = [
    "XOM",
    "CVX",
    "COP",
    "WMB",
    "EOG",
    "GEV",
    "CEG",
    "VST",
    "MPC",
    "PSX",
    "SLB",
]

Base.metadata.create_all(bind=engine)


@app.post("/stocksall")
async def stockdata(db: Session = Depends(get_db)):
    results = {}
    stored_count = 0
    async with httpx.AsyncClient() as client:
        for symbol in stocklist:
            fetch_url = f"{BASE_URL}?identifier={symbol}&key={API_KEY}"
            response = await client.get(fetch_url)
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                record = data[0]
                stock = models.StockPrice(
                    trading_symbol=symbol,
                    date=record["date"],
                    open=float(record["open"]) if record["open"] else 0.0,
                    high=float(record["high"]) if record["high"] else 0.0,
                    low=float(record["low"]) if record["low"] else 0.0,
                    close=float(record["close"]) if record["close"] else 0.0,
                    volume=int(float(record["volume"])) if record["volume"] else 0,
                )
                db.add(stock)
                stored_count += 1
                print(f"Added {symbol} to database session")
            else:
                print(f"No data found for {symbol} response is not a list or is empty")

            results[symbol] = data

    if stored_count > 0:
        db.commit()
        print(f"Successfully committed {stored_count} records to database")
    else:
        print("No records to commit")

    return {
        "message": "Processing complete",
        "stored_symbols": list(results.keys()),
        "stored_count": stored_count,
        "results": results,
    }


@app.get("/stocks/{symbol}")
async def getstock(symbol: str, db: Session = Depends(get_db)):
    stock = (
        db.query(models.StockPrice)
        .filter(models.StockPrice.trading_symbol == symbol)
        .order_by(models.StockPrice.date.desc())
        .first()
    )

    if stock:
        return {
            "symbol": symbol,
            "data": {
                "date": stock.date,
                "open": stock.open,
                "high": stock.high,
                "low": stock.low,
                "close": stock.close,
                "volume": stock.volume,
            },
        }

    return {"message": f"No data found for {symbol}"}

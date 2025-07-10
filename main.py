from typing import Union
from fastapi import FastAPI
import yfinance as yf

data = yf.Ticker("MSFT")

app = FastAPI()


@app.get("/")
def read_root():
    return {"ticker": data.info}
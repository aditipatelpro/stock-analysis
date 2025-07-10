from typing import Union
from fastapi import FastAPI
import getpass
import os
from dotenv import load_dotenv
import yfinance as yf

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = init_chat_model("gpt-4o-mini", model_provider="openai")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome to stock-analysis"}

@app.get("/tickers/{ticker}")
def read_ticker(ticker: str):
    ticker_data = yf.Ticker(ticker)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Provide me a short stock valuation summary in a single plain text paragraph on the fundamental data from {ticker_info}.")
    ])
    prompt = prompt_template.invoke({"ticker_info": ticker_data.info})

    ai_message = model.invoke(prompt)

    return {"summary": ai_message.content}
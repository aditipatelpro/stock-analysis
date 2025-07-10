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
    data = yf.Ticker(ticker)

    system_template = "Provide me a brief valution summary for {value}"
    prompt_template = ChatPromptTemplate.from_messages([("system", system_template)])
    prompt = prompt_template.invoke({"value": ticker})

    response = model.invoke(prompt)

    return {"Summary": response.content}
#this is the "app/fx-intraday.py" file...
import json
from pprint import pprint
from statistics import mean

import requests
from plotly.express import line

from pandas import read_csv
from app.alpha import API_KEY

def fetch_exchange_data(fromCurrency,toCurrency):
    request_url = f"https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol={fromCurrency}&to_symbol={toCurrency}&interval=60min&outputsize=full&apikey={API_KEY}&datatype=csv"
    print(request_url)
    df = read_csv(request_url)
    return df



if __name__ == "__main__":
    print("FX REPORT...")

    fromCurrency = input("Please input a currency symbol you want to exchange from (default: 'USD')") or "USD"
    print("Exchange from: ",fromCurrency)

    toCurrency = input("Please input a currency symbol you want to exchange to (default: 'EUR')") or "EUR"
    print ("Exchange to :", toCurrency)

    df = fetch_exchange_data(fromCurrency,toCurrency)
    print(df)
    
    print(df.columns)
    print(df.head())

    latest = df.iloc[0]

    print("LATEST EXCHANGE RATE FROM",fromCurrency," TO ",toCurrency,":",latest["close"],"as of", latest["timestamp"])
    
    dates = df["timestamp"]
  
    rates = df["close"]

    fig = line(x=dates, y=rates, title="Weekly Exchange Rate", labels= {"x": "Month", "y": "Exchange Rate"})
    fig.show()
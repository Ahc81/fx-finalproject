#this is the "app/fxintraday.py" file...
import json
from pprint import pprint
from statistics import mean

import requests
from plotly.express import line

from pandas import read_csv
from app.alpha import API_KEY

def fetch_exchange_data(combinedTimeFrame,fromCurrency,toCurrency):

    request_url = f"https://www.alphavantage.co/query?function={combinedTimeFrame}&from_symbol={fromCurrency}&to_symbol={toCurrency}&interval=60min&outputsize=full&apikey={API_KEY}&datatype=csv"
    print(request_url)
    df = read_csv(request_url)
    return df



if __name__ == "__main__":
    print("FX REPORT...")

    fromCurrency = input("Please input a currency symbol you want to exchange from (default: 'USD')") or "USD"
    print("Exchange from: ",fromCurrency)

    toCurrency = input("Please input a currency symbol you want to exchange to (default: 'EUR')") or "EUR"
    print ("Exchange to :", toCurrency)

    timeFrame = input("Please input your selected timing of your exchange data (ie. Intraday, Daily, Weekly, Monthly: ").upper()
    timeFrameAsString = str(timeFrame)
    combinedTimeFrame = str("FX_") + timeFrameAsString
    print(str(combinedTimeFrame))
    
    df = fetch_exchange_data(combinedTimeFrame,fromCurrency,toCurrency)
    print(df)
    
    print(df.columns)
    print(df.head())

    latest = df.iloc[0]

    print("LATEST EXCHANGE RATE FROM",fromCurrency," TO ",toCurrency,":",latest["close"],"as of", latest["timestamp"])
    
    dates = df["timestamp"]
  
    rates = df["close"]
    chartName = timeFrameAsString + " Exchange Rate"
    if timeFrameAsString == "DAILY":
        xAxis = "Days"
    elif timeFrameAsString == "INTRADAY":
        xAxis = "Times"
    elif timeFrameAsString == "WEEKLY":
        xAxis = "Weeks"
    elif timeFrameAsString == "MONTHLY":
        xAxis = "Months"
        

    fig = line(x=dates, y=rates, title=chartName, labels= {"x": xAxis, "y": "Exchange Rate"})
    fig.show()
    
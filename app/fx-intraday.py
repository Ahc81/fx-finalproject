#this is the "app/fx-intraday.py" file...

from pandas import read_csv
from app.alpha import API_KEY

def fetch_exchange_data(fromCurrency,toCurrency):
    request_url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={fromCurrency}&to_symbol={toCurrency}&interval=5min&outputsize=full&apikey={API_KEY}&datatype=csv"
    df = read_csv(request_url)
    return df

if __name__ == "__main__":
    print("FX REPORT...")

    fromCurrency = input("Please input a currency symbol you want to exchange from (default: 'EUR')") or "EUR"
    print("Exchange from: ",fromCurrency)

    toCurrency = input("Please input a currency symbol you want to exchange to (default: 'USD") or "USD"
    print ("Exchange to :", toCurrency)

    df= fetch_exchange_data(fromCurrency,toCurrency)

    latest = df.iloc[0]

    print("LATEST:",latest["close"],"as of", latest["timestamp"])

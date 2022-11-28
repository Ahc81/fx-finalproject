from plotly.express import line
from pandas import read_csv
from app.alpha import API_KEY

#function to fetch the exchange rate data
def fetch_exchange_data(combinedTimeFrame,fromCurrency,toCurrency):
#API key from app.alpha and from .env before that
    request_url = f"https://www.alphavantage.co/query?function={combinedTimeFrame}&from_symbol={fromCurrency}&to_symbol={toCurrency}&interval=60min&outputsize=full&apikey={API_KEY}&datatype=csv"
    print(request_url)
    df = read_csv(request_url)
    return df #stores data as dataframe

def calculate_new_currency(fromCurrencyAmount,latestClose):
    newCurrencyAmount = fromCurrencyAmount * latestClose
    return newCurrencyAmount

#Begin main body
if __name__ == "__main__":
    print("FX REPORT...")
#inputs the currency you want to convert from
    fromCurrency = input("Please input a currency symbol you want to exchange from (default: 'USD')") or "USD"
    print("Exchange from: ",fromCurrency)
#inputs the currency you want to convert to
    toCurrency = input("Please input a currency symbol you want to exchange to (default: 'EUR')") or "EUR"
    print ("Exchange to :", toCurrency)
#Input what type of time frame you want
   
    timeFrameAsString = str("INTRADAY")
    combinedTimeFrame = str("FX_") + timeFrameAsString
    print(str(combinedTimeFrame))
    #data fetching function
    df = fetch_exchange_data(combinedTimeFrame,fromCurrency,toCurrency)
    
    latest = df.iloc[0]
    
    #sorting through the dataframe
    print("LATEST EXCHANGE RATE FROM",fromCurrency," TO ",toCurrency,":",latest["close"],"as of", latest["timestamp"])
    
    latestClose = eval(latest["close"])
    fromCurrencyAmount = eval(input("Input how many ", fromCurrency," you would like converted: " ))
    newCurrencyAmount = calculate_new_currency(fromCurrencyAmount, latestClose)
    print("You can convert to ",newCurrencyAmount," ",fromCurrency,".")
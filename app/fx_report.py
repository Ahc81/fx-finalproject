#this is the "app/fx_report.py" file...
#imported packages
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

#Calculataes the appreciation or depreciation of the currency over time against an inputted benchmark
def appreciate_or_depreciate(latestClose,firstClose,fromCurrency,toCurrency,firstDate):
    appreciationAmount = latestClose/firstClose -1
    appreciationAmountRounded = round(appreciationAmount,2)
    appreciationAmountAsPercent = str(appreciationAmountRounded*100)+"%" 
    if appreciationAmount > 0:
        result = -1
        ("The" , fromCurrency , "has depreciated against the" , toCurrency , " by", appreciationAmountAsPercent , "since ", firstDate , ".")
    elif appreciationAmount<0:
        result = 1
        ("The ", fromCurrency, " has appreciated against the ",toCurrency, " by", appreciationAmountAsPercent,"since ", firstDate, ".")

    return result
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
    timeFrame = input("Please input your selected timing of your exchange data (ie. Intraday, Daily, Weekly, Monthly: ").upper()
    timeFrameAsString = str(timeFrame)
    combinedTimeFrame = str("FX_") + timeFrameAsString
    print(str(combinedTimeFrame))
    #data fetching function
    df = fetch_exchange_data(combinedTimeFrame,fromCurrency,toCurrency)
    print(df)
    
    print(df.columns)
    print(df.head())

    latest = df.iloc[0]
    first = df.iloc[-1]
    #sorting through the dataframe
    print("LATEST EXCHANGE RATE FROM",fromCurrency," TO ",toCurrency,":",latest["close"],"as of", latest["timestamp"])
    
    latestClose = latest["close"]
    print(latestClose)
    firstClose = first["close"]
    print(firstClose)
    firstDate = first["timestamp"]
    print(firstDate)
    #appreciation calculation
    result = appreciate_or_depreciate(latestClose, firstClose, fromCurrency,toCurrency,firstDate)
    print(result)
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
#chart or no chart
    chart = input("Would you like a chart to be made? (Y/N) ")

    if chart == "Y" or "y" or "yes":

        fig = line(x=dates, y=rates, title=chartName, labels= {"x": xAxis, "y": "Exchange Rate"})
        fig.show()
        print("Thank you for using the program.")
        print("We hope you had a good experience.")
        print("Happy exchanging!")

    else:
        print("Thank you for using the program.")
        print("We hope you had a good experience.")
        print("Happy exchanging!")

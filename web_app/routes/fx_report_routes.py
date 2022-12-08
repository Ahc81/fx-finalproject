

from flask import Blueprint, request, render_template, redirect, flash

from app.fx_report import fetch_exchange_data, appreciate_or_depreciate
from plotly.express import line
from pandas import read_csv

fx_report_routes = Blueprint("fx_report_routes", __name__)

@fx_report_routes.route("/fx_report/form")
def fx_report_form():
    return render_template("fx_report_form.html")

@fx_report_routes.route("/fx_report/dashboard", methods=["GET", "POST"])
def fx_report_dashboard():
    print("FX Dashboard...")


    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    fromCurrencySymbol = request_data.get("From Currency") or "USD"
    toCurrencySymbol = request_data.get("To Currency") or "EUR"
    timeFrame = request_data.get("Monthly, Weekly, Daily, or Intraday") or "INTRADAY"
    timeFrameAsString = str(timeFrame).upper()
    combinedTimeFrame = str("FX_") + timeFrameAsString
    if timeFrameAsString == "DAILY":
                    xAxis = "Days"
    elif timeFrameAsString == "INTRADAY":
        xAxis = "Times"
    elif timeFrameAsString == "WEEKLY":
        xAxis = "Weeks"
    elif timeFrameAsString == "MONTHLY":
        xAxis = "Months"
    try:
        df = fetch_exchange_data(combinedTimeFrame = combinedTimeFrame, fromCurrency = fromCurrencySymbol, toCurrency = toCurrencySymbol)
        latest = df.iloc[0]
        first = df.iloc[-1]
        latestClose = latest["close"]
        firstClose = first["close"]
        firstDate = first["timestamp"]
        dates =  df["timestamp"]
        rates = df["close"]
        chartName = timeFrameAsString + " Exchange Rate"
        fig = line(x=dates, y=rates, title=chartName, labels= {"x": xAxis, "y": "Exchange Rate"})
        

        flash("Fetched Latest Unemployment Data!", "success")
        return render_template("fx_dashboard.html",
            fromCurrencySymbol = fromCurrencySymbol,
            toCurrencySymbol = toCurrencySymbol,
            latestClose = latestClose,
            firstClose = firstClose,
            firstDate = firstDate,
            chartName = timeFrameAsString + " Exchange Rate",
            fig = fig
        )
    except Exception as err:
        print('OOPS', err)

        flash("FX Data Error. Please try again!", "danger")
        return redirect("/")

#
# API ROUTES
#

@fx_report_routes.route("/api/fx.json")
def fx_api():
    print("FX DATA (API)...")

    # for data supplied via GET request, url params are in request.args:
    url_params = dict(request.args)
    print("URL PARAMS:", url_params)
    fromCurrencySymbol = url_params.get("fromCurrencySymbol") or "USD"
    toCurrencySymbol = url_params.get("toCurrencySymbol") or "EUR"
    timeFrame = url_params.get("timeFrame") or "INTRADAY"
    timeFrameAsString = str(timeFrame).upper()
    combinedTimeFrame = str("FX_") + timeFrameAsString

    try:
        df = fetch_exchange_data(combinedTimeFrame = combinedTimeFrame, fromCurrency = fromCurrencySymbol, toCurrency = toCurrencySymbol)
        data = df.to_dict("records")
        return {"combinedTimeFrame":combinedTimeFrame,"fromCurrencySymbol": fromCurrencySymbol,"toCurrencySymbol": toCurrencySymbol, "data": data }
    except Exception as err:
        print('OOPS', err)
        return {"message":"Market Data Error. Please try again."}, 404
# this is the "web_app/routes/stocks_routes.py" file ...

from flask import Blueprint, request, render_template, redirect, flash

from app.fx_calculate import fetch_exchange_data, calculate_new_currency

fx_calculate_routes = Blueprint("fx_calculate_routes", __name__)

@fx_calculate_routes.route("/fx_calculate/form")
def fx_calculate_form():
    print("FX Calculator...")
    return render_template("fx_form.html")

@fx_calculate_routes.route("/fx/dashboard", methods=["GET", "POST"])
def fx_calculate_dashboard():
    print("FX Calculator Dashboard...")

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
    fromCurrencyAmount = request_data.get("From Currency Amount") or "100"

    try:
        df = fetch_exchange_data(combinedTimeFrame="FX_INTRADAY",fromCurrency=fromCurrencySymbol,toCurrency=toCurrencySymbol)
        latest = df.iloc[0]
        latestClose = latest["close"]
        newCurrencyAmount=calculate_new_currency(fromCurrencyAmount=fromCurrencyAmount, latestClose=latestClose)

        #flash("Fetched Real-time Market Data!", "success")
        return render_template("fx_dashboard.html",
            fromCurrency=fromCurrencySymbol,
            latestClose=latestClose,
            newCurrencyAmount=newCurrencyAmount
        )
    except Exception as err:
        print('OOPS', err)

        flash("Market Data Error. Please check your symbol and try again!", "danger")
        return redirect("/fx_calculate/form")

#
# API ROUTES
#

@fx_calculate_routes.route("/api/fx.json")
def fx_api():
    print("FX DATA (API)...")

    # for data supplied via GET request, url params are in request.args:
    url_params = dict(request.args)
    print("URL PARAMS:", url_params)
    symbol = url_params.get("from currency") or "USD"

    try:
        df = fetch_exchange_data(symbol=symbol)
        data = df.to_dict("records")
        return {"symbol": symbol, "data": data }
    except Exception as err:
        print('OOPS', err)
        return {"message":"Market Data Error. Please try again."}, 404
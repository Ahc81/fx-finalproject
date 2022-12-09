# this is the "web_app/routes/stocks_routes.py" file ...

from flask import Blueprint, request, render_template, redirect, flash

from app.fx_calculate import fetch_exchange_data, calculate_new_currency

fx_calculate_routes = Blueprint("fx_calculate_routes", __name__)

@fx_calculate_routes.route("/fx_calculate/form")
def fx_calculate_form():
    print("FX Calculator...")
    return render_template("fx_calculate_form.html")

@fx_calculate_routes.route("/fx_calculate/dashboard", methods=["GET", "POST"])
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
        print(latestClose)
        print(fromCurrencyAmount)
        print(toCurrencySymbol)
        newCurrencyAmount=calculate_new_currency(fromCurrencyAmount=fromCurrencyAmount, latestClose=latestClose)

        flash("Fetched Real-time Market Data!", "success")
        return render_template("fx_form_output.html",
            fromCurrency=fromCurrencySymbol,
            toCurrency=toCurrencySymbol,
        
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

from flask import Blueprint, request, render_template, redirect, flash

from app.fx_report import fetch_exchange_data, appreciate_or_depreciate

fx_report_routes = Blueprint("fx_report_routes", __name__)

@fx_report_routes.route("/fx/form")
def stocks_form():
    print("FX FORM...")
    return render_template("fx_form.html")

@fx_report_routes.route("/fx/dashboard", methods=["GET", "POST"])
def FX_dashboard():
    print("FX DASHBOARD...")

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    fromCurrencySymbol = request_data.get("symbol") or "USD"

    try:
        df = fetch_exchange_data(symbol=fromCurrencySymbol,)
        latest_close = (df.iloc[0]["close"])
        latest_date = df.iloc[0]["timestamp"]
        data = df.to_dict("records")

        #flash("Fetched Real-time Market Data!", "success")
        return render_template("fx_dashboard.html",
            symbol=fromCurrencySymbol,
            latest_close=latest_close,
            latest_date=latest_date,
            data=data
        )
    except Exception as err:
        print('OOPS', err)

        #flash("Market Data Error. Please check your symbol and try again!", "danger")
        return redirect("/fx/form")

#
# API ROUTES
#

@fx_report_routes.route("/api/stocks.json")
def stocks_api():
    print("STOCKS DATA (API)...")

    # for data supplied via GET request, url params are in request.args:
    url_params = dict(request.args)
    print("URL PARAMS:", url_params)
    symbol = url_params.get("symbol") or "NFLX"

    try:
        df = fetch_exchange_data(symbol=symbol)
        data = df.to_dict("records")
        return {"symbol": symbol, "data": data }
    except Exception as err:
        print('OOPS', err)
        return {"message":"Market Data Error. Please try again."}, 404
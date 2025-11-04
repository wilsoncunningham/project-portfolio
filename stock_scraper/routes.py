from flask import render_template, request
from pprint import pprint
from . import bp
from .scraper import scrape_ticker

@bp.route("/", methods=["GET", "POST"])
def stocks():
    data = None
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker", "").strip()
        if not ticker:
            error = "Please enter a ticker."
        else:
            try:
                data = scrape_ticker(ticker)
                if not data.get("price"):
                    error = "Could not find price for that ticker."
                pprint(data)
            except Exception as e:
                error = f"Error fetching ticker: {e}"

    return render_template("stock_scraper.html", data=data, error=error)

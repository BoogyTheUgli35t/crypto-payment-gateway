import os
from flask import Flask, request, render_template, redirect
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Flask app setup
app = Flask(__name__)

# NOWPayments API Key from .env
API_KEY = os.getenv("NOWPAYMENTS_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = request.form.get("amount")

        payload = {
            "price_amount": float(amount),
            "price_currency": "usd",
            "pay_currency": "btc",
            "ipn_callback_url": "https://yourdomain.com/ipn",
            "order_id": "1234",
            "order_description": "Test payment"
        }

        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post("https://api.nowpayments.io/v1/payment", json=payload, headers=headers)
            data = response.json()

            if "invoice_url" not in data:
                return f"<h2>NOWPayments Error:</h2><pre>{data}</pre>", 500

            return redirect(data["invoice_url"])
        except Exception as e:
            return f"<h2>Internal Server Error:</h2><pre>{str(e)}</pre>", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


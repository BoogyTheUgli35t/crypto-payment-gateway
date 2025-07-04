import os
from flask import Flask, request, render_template, redirect
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)

# ✅ CORRECT: get value from ENV VAR named 'NOWPAYMENTS_API_KEY'
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
        response = requests.post("https://api.nowpayments.io/v1/payment", json=payload, headers=headers)
        data = response.json()

        # Handle API error (optional)
        if "invoice_url" not in data:
            return f"Error: {data}", 500

        return redirect(data["invoice_url"])
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

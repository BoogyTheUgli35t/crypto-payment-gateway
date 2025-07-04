 
import os
from flask import Flask, request, render_template, redirect
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("AY7V4ZP-DQKMS08-HARPVTJ-52WWMFE")

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
        return redirect(data["invoice_url"])
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

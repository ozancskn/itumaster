from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/UserService")
def user_service():
    return render_template("user.html")

@app.route("/RestourantService")
def restourant_service():
    return render_template("restaurant.html")

@app.route("/OrderService")
def order_service():
    return "Order Service.."

@app.route("/PaymentService")
def payment_service():
    return "Payment Service.."

@app.route("/DeliveryService")
def delivery_service():
    return render_template("delivery.html")

@app.route("/NotificationService")
def notification_service():
    return "Notification Service.."

@app.route("/register")
def register_service():
    response= requests.get("http://localhost:5001/register")
    return response.text, response.status_code


if __name__ == "__main__":
    app.run(debug=True)
    
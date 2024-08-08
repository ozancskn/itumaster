#api_gateway.py
from flask import Flask, render_template, request, jsonify, Response
import requests
from flask import session as flask_session
import json

app = Flask(__name__)
app.secret_key = 'gizli_anahtar_buraya'
@app.route("/")
def index():
    response = requests.get("http://home_page:5008/")
    return response.text, response.status_code

@app.route("/UserService", methods=['GET', 'POST'])
def user_service():
    response = requests.get("http://localhost:5001/UserService")
    return response.text, response.status_code

@app.route("/RestaurantService/<path:subpath>", methods=['GET', 'POST'])
def restaurant_service(subpath):
    url = f"http://restaurant_service:5002/RestaurantService/{subpath}"

    if request.method == 'GET':
        response = requests.get(url, params=request.args)
    elif request.method == 'POST':
        response = requests.post(url, data=request.form)
    else:
        return "Method not allowed", 405

    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/OrderService", defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route("/OrderService/<path:subpath>", methods=['GET', 'POST'])
def order_service(subpath):
    url = f"http://order_service:5003/OrderService/{subpath}"

    if request.method == 'GET':
        response = requests.get(url, params=request.args)
    elif request.method == 'POST':
        response = requests.post(url, data=request.form)
    else:
        return "Method not allowed", 405

    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/add_to_cart", methods=['POST'])
def add_to_cart_gateway():
    url = "http://order_service:5003/OrderService/add_to_cart"
    # Oturum verilerini istek başlıklarına ekleyelim
    headers = {'X-Session-Cart': json.dumps(flask_session.get('cart', []))}
    response = requests.post(url, data=request.form, headers=headers)
    # Yanıttaki oturum verilerini güncelleyelim
    if 'X-Session-Cart' in response.headers:
        flask_session['cart'] = json.loads(response.headers['X-Session-Cart'])
    return Response(response.content, status=response.status_code, headers=dict(response.headers))
@app.route("/cart")
def view_cart_gateway():
    url = "http://order_service:5003/cart"
    # Oturum verilerini istek başlıklarına ekleyelim
    headers = {'X-Session-Cart': json.dumps(flask_session.get('cart', []))}
    response = requests.get(url, headers=headers)
    # Yanıttaki oturum verilerini güncelleyelim
    if 'X-Session-Cart' in response.headers:
        flask_session['cart'] = json.loads(response.headers['X-Session-Cart'])
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/remove_from_cart", methods=['POST'])
def remove_from_cart_gateway():
    url = "http://order_service:5003/remove_from_cart"
    response = requests.post(url, data=request.form)
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/PaymentService")
def payment_service():
    response = requests.get("http://localhost:5004/PaymentService")
    return response.text, response.status_code

@app.route("/DeliveryService")
def delivery_service():
    response = requests.get("http://localhost:5005/DeliveryService")
    return response.text, response.status_code

@app.route("/NotificationService")
def notification_service():
    response = requests.get("http://localhost:5006/NotificationService")
    return response.text, response.status_code

@app.route("/register", methods=['GET', 'POST'])
def register_service():
    if request.method == 'POST':
        response = requests.post("http://localhost:5007/register", data=request.form)
    else:
        response = requests.get("http://localhost:5007/register")
    return response.text, response.status_code

@app.route("/login", methods=['GET', 'POST'])
def login_service():
    if request.method == 'POST':
        response = requests.post("http://localhost:5007/login", data=request.form)
    else:
        response = requests.get("http://localhost:5007/login")
    return response.text, response.status_code

@app.route("/logout")
def logout():
    response = requests.post("http://localhost:5007/logout")
    return response.text, response.status_code

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
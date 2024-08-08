from flask import Flask, render_template

app = Flask(__name__)


@app.route("/DeliveryService")
def register_service():
    return render_template("delivery.html")

if __name__ == '__main__':
    app.run(debug=True, port=5005)


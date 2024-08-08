from flask import Flask, render_template, session, redirect, request, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Gerçek bir uygulama için güvenli bir anahtar kullanın

# Diğer servislerin URL'leri
AUTH_SERVICE_URL = "http://localhost:5000"  # authentication.py'nin çalıştığı port

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Please log in to access this page.', 'warning')
            return redirect(f"{AUTH_SERVICE_URL}/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/UserService")
@login_required
def user_service():
    return render_template("user.html", username=session.get('username'), auth_service_url=AUTH_SERVICE_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
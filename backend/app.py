from flask import Flask, render_template, jsonify
from database import get_db_connection
from routes.auth import auth_bp
from routes.pharmacy import pharmacy_bp
from routes.ngo import ngo_bp

# Create Flask app
app = Flask(__name__)
app.secret_key = "medibridge-secret-key-change-in-production"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(pharmacy_bp)
app.register_blueprint(ngo_bp)

# --- Page Routes (GET only, serve HTML) ---

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/pharmacy-dashboard")
def pharmacy_dashboard():
    return render_template("pharmacy_dashboard.html")

@app.route("/ngo-dashboard")
def ngo_dashboard():
    return render_template("ngo_dashboard.html")

@app.route("/pharmacy-requests-page")
def pharmacy_requests_page():
    return render_template("pharmacy_requests.html")

@app.route("/ngo-requests-page")
def ngo_requests_page():
    return render_template("ngo_requests.html")

# --- Global Error Handlers ---

@app.errorhandler(404)
def not_found(e):
    return jsonify({"message": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)

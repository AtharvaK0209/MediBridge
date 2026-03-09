from flask import Flask
from database import get_db_connection
from flask import Flask, render_template
from routes.auth import auth_bp
from routes.pharmacy import pharmacy_bp


# Create Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(pharmacy_bp)

@app.route("/")
def home():
    return "Backend is running cleanly!"

# checking db connection
@app.route("/test-db")
def test_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        conn.close()
        return str(tables)
    return "Database connection failed"

# home route to render the home page
@app.route("/home")
def home_page():
    return render_template("index.html")

# register route to render the registration page
@app.route("/register-page")
def register_page():
    return render_template("register.html")

# login route to render the login page
@app.route("/login-page")
def login_page():
    return render_template("login.html")

# pharmacy dashboard route to render the pharmacy dashboard page
@app.route("/pharmacy-dashboard")
def pharmacy_dashboard():
    return render_template("pharmacy_dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)

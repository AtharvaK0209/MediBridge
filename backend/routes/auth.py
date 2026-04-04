from flask import Blueprint, request, jsonify
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    role = data.get("role", "").strip()
    org_name = data.get("org_name", "").strip()
    address = data.get("address", "").strip()
    contact = data.get("contact", "").strip()

    # Input validation
    if not all([name, email, password, role]):
        return jsonify({"message": "Name, email, password and role are required"}), 400

    if role not in ("pharmacy", "ngo"):
        return jsonify({"message": "Role must be 'pharmacy' or 'ngo'"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # Hash the password before storing
        hashed_pw = generate_password_hash(password)

        # Insert into users table
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (name, email, hashed_pw, role))

        user_id = cursor.lastrowid

        # Insert into pharmacy or ngo table
        if role == "pharmacy":
            cursor.execute("""
                INSERT INTO pharmacy (user_id, pharmacy_name, address, contact)
                VALUES (%s, %s, %s, %s)
            """, (user_id, org_name, address, contact))

        elif role == "ngo":
            cursor.execute("""
                INSERT INTO ngo (user_id, ngo_name, address, contact)
                VALUES (%s, %s, %s, %s)
            """, (user_id, org_name, address, contact))

        conn.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


# LOGIN
@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM users WHERE email=%s
        """, (email,))

        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            return jsonify({
                "message": "Login successful",
                "role": user["role"],
                "user_id": user["user_id"]
            }), 200

        return jsonify({"message": "Invalid credentials"}), 401

    finally:
        cursor.close()
        conn.close()
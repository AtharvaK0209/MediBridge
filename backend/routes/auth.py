from flask import Blueprint, request, jsonify
from database import get_db_connection

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register-page", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    org_name = data.get("org_name")
    address = data.get("address")
    contact = data.get("contact")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into users table
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (name, email, password, role))

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
@auth_bp.route("/login-page", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM users WHERE email=%s AND password=%s
    """, (email, password))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "role": user["role"],
            "user_id": user["user_id"]
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401
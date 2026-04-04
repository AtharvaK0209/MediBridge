from flask import Blueprint, request, jsonify
from database import get_db_connection
from datetime import datetime
from email_service import send_expiry_alert

pharmacy_bp = Blueprint("pharmacy", __name__)

@pharmacy_bp.route("/api/add-medicine", methods=["POST"])
def add_medicine():
    data = request.get_json()

    medicine_name = data.get("medicine_name", "").strip()
    quantity = data.get("quantity")
    expiry_date = data.get("expiry_date")
    original_price = data.get("original_price")
    discount_price = data.get("discount_price")
    user_id = data.get("user_id")

    if not all([medicine_name, quantity, expiry_date, original_price, discount_price, user_id]):
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # Get pharmacy_id
        cursor.execute("SELECT pharmacy_id FROM pharmacy WHERE user_id=%s", (user_id,))
        pharmacy = cursor.fetchone()

        if not pharmacy:
            return jsonify({"message": "Pharmacy not found"}), 400

        pharmacy_id = pharmacy[0]

        # Determine status
        today = datetime.today().date()
        exp_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

        if exp_date < today:
            status = "EXPIRED"
        elif (exp_date - today).days <= 30:
            status = "NEAR_EXPIRY"
        else:
            status = "SAFE"

        cursor.execute("""
            INSERT INTO medicines
            (pharmacy_id, medicine_name, quantity, expiry_date,
             original_price, discount_price, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            pharmacy_id,
            medicine_name,
            quantity,
            expiry_date,
            original_price,
            discount_price,
            status
        ))

        conn.commit()
        return jsonify({"message": "Medicine added successfully"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


@pharmacy_bp.route("/api/get-medicines/<int:user_id>")
def get_medicines(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT m.*
            FROM medicines m
            JOIN pharmacy p ON m.pharmacy_id = p.pharmacy_id
            WHERE p.user_id=%s
            ORDER BY m.expiry_date ASC
        """, (user_id,))

        medicines = cursor.fetchall()

        expired = 0
        near = 0

        for med in medicines:
            if med["status"] == "EXPIRED":
                expired += 1
            elif med["status"] == "NEAR_EXPIRY":
                near += 1

        # get user email and send alert (kept as-is per user request)
        cursor.execute("SELECT email FROM users WHERE user_id=%s", (user_id,))
        user = cursor.fetchone()

        if user:
            email = user["email"]
            if expired > 0 or near > 0:
                send_expiry_alert(email, expired, near)

        return jsonify(medicines)

    finally:
        cursor.close()
        conn.close()


@pharmacy_bp.route("/api/delete-medicine/<int:medicine_id>", methods=["DELETE"])
def delete_medicine(medicine_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM medicines WHERE medicine_id=%s", (medicine_id,))
        conn.commit()
        return jsonify({"message": "Medicine deleted"})

    finally:
        cursor.close()
        conn.close()


@pharmacy_bp.route("/api/pharmacy-requests/<int:user_id>")
def pharmacy_requests(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        # Get pharmacy_id
        cursor.execute("SELECT pharmacy_id FROM pharmacy WHERE user_id=%s", (user_id,))
        pharmacy = cursor.fetchone()

        if not pharmacy:
            return jsonify({"message": "Pharmacy not found"}), 400

        pharmacy_id = pharmacy["pharmacy_id"]

        # Get requests for this pharmacy
        cursor.execute("""
            SELECT r.request_id, r.requested_quantity, r.status,
                   m.medicine_name, m.medicine_id,
                   n.ngo_name
            FROM redistribution_requests r
            JOIN medicines m ON r.medicine_id = m.medicine_id
            JOIN ngo n ON r.ngo_id = n.ngo_id
            WHERE m.pharmacy_id=%s
            ORDER BY r.request_id DESC
        """, (pharmacy_id,))

        requests = cursor.fetchall()
        return jsonify(requests)

    finally:
        cursor.close()
        conn.close()


@pharmacy_bp.route("/api/update-request", methods=["POST"])
def update_request():
    data = request.get_json()

    request_id = data.get("request_id")
    action = data.get("action")  # APPROVED or REJECTED

    if action not in ("APPROVED", "REJECTED"):
        return jsonify({"message": "Invalid action"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # Update request status
        cursor.execute("""
            UPDATE redistribution_requests
            SET status=%s
            WHERE request_id=%s
        """, (action, request_id))

        # If approved → reduce stock and insert into transactions
        if action == "APPROVED":
            cursor.execute("""
                SELECT medicine_id, ngo_id, requested_quantity
                FROM redistribution_requests
                WHERE request_id=%s
            """, (request_id,))

            req = cursor.fetchone()

            if req:
                medicine_id, ngo_id, qty = req

                # Check available stock before reducing
                cursor.execute("SELECT quantity FROM medicines WHERE medicine_id=%s", (medicine_id,))
                med = cursor.fetchone()

                if med and med[0] >= qty:
                    # Reduce stock
                    cursor.execute("""
                        UPDATE medicines
                        SET quantity = quantity - %s
                        WHERE medicine_id=%s
                    """, (qty, medicine_id))

                    # Insert transaction
                    cursor.execute("""
                        INSERT INTO transactions
                        (medicine_id, ngo_id, quantity)
                        VALUES (%s,%s,%s)
                    """, (medicine_id, ngo_id, qty))
                else:
                    conn.rollback()
                    return jsonify({"message": "Insufficient stock"}), 400

        conn.commit()
        return jsonify({"message": f"Request {action.lower()}"})

    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        conn.close()
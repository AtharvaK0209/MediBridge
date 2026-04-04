from flask import Blueprint, request, jsonify
from database import get_db_connection

ngo_bp = Blueprint("ngo", __name__)

@ngo_bp.route("/api/available-medicines")
def available_medicines():
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT m.medicine_id, m.medicine_name, m.quantity, m.expiry_date,
                   m.original_price, m.discount_price, m.status, m.pharmacy_id,
                   p.pharmacy_name
            FROM medicines m
            JOIN pharmacy p ON m.pharmacy_id = p.pharmacy_id
            WHERE m.status IN ('SAFE', 'NEAR_EXPIRY')
            AND m.quantity > 0
            ORDER BY m.expiry_date ASC
        """)

        data = cursor.fetchall()
        return jsonify(data)

    finally:
        cursor.close()
        conn.close()


@ngo_bp.route("/api/request-medicine", methods=["POST"])
def request_medicine():
    data = request.get_json()

    medicine_id = data.get("medicine_id")
    ngo_user_id = data.get("ngo_id")
    quantity = data.get("quantity")

    if not all([medicine_id, ngo_user_id, quantity]):
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT ngo_id FROM ngo WHERE user_id=%s", (ngo_user_id,))
        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"message": "NGO not found"}), 400

        ngo_id = ngo[0]

        # Validate requested quantity against available stock
        cursor.execute("SELECT quantity FROM medicines WHERE medicine_id=%s", (medicine_id,))
        med = cursor.fetchone()

        if not med:
            return jsonify({"message": "Medicine not found"}), 404

        if int(quantity) > med[0]:
            return jsonify({"message": f"Only {med[0]} units available"}), 400

        if int(quantity) <= 0:
            return jsonify({"message": "Quantity must be greater than 0"}), 400

        cursor.execute("""
            INSERT INTO redistribution_requests
            (medicine_id, ngo_id, requested_quantity)
            VALUES (%s,%s,%s)
        """, (medicine_id, ngo_id, quantity))

        conn.commit()
        return jsonify({"message": "Request sent successfully"})

    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


@ngo_bp.route("/api/ngo-stats/<int:user_id>")
def ngo_stats(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        # Get NGO ID
        cursor.execute("SELECT ngo_id FROM ngo WHERE user_id=%s", (user_id,))
        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"message": "NGO not found"}), 400

        ngo_id = ngo["ngo_id"]

        # Single optimized query instead of two separate ones
        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END) AS approved
            FROM redistribution_requests
            WHERE ngo_id=%s
        """, (ngo_id,))
        stats = cursor.fetchone()

        return jsonify({
            "total_requests": stats["total"] or 0,
            "approved_requests": stats["approved"] or 0
        })

    finally:
        cursor.close()
        conn.close()


@ngo_bp.route("/api/pharmacies")
def get_pharmacies():
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT pharmacy_id, pharmacy_name, address, contact
            FROM pharmacy
        """)

        data = cursor.fetchall()
        return jsonify(data)

    finally:
        cursor.close()
        conn.close()


@ngo_bp.route("/api/pharmacy-medicines/<int:pharmacy_id>")
def pharmacy_medicines(pharmacy_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT medicine_id, medicine_name, quantity, expiry_date,
                   original_price, discount_price, status
            FROM medicines
            WHERE pharmacy_id=%s
            AND status != 'EXPIRED'
            AND quantity > 0
            ORDER BY expiry_date ASC
        """, (pharmacy_id,))

        data = cursor.fetchall()
        return jsonify(data)

    finally:
        cursor.close()
        conn.close()


@ngo_bp.route("/api/my-requests/<int:user_id>")
def my_requests(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        # Get NGO ID
        cursor.execute("SELECT ngo_id FROM ngo WHERE user_id=%s", (user_id,))
        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"message": "NGO not found"}), 400

        ngo_id = ngo["ngo_id"]

        # Get requests
        cursor.execute("""
            SELECT r.request_id, r.requested_quantity, r.status,
                   m.medicine_name
            FROM redistribution_requests r
            JOIN medicines m ON r.medicine_id = m.medicine_id
            WHERE r.ngo_id=%s
            ORDER BY r.request_id DESC
        """, (ngo_id,))

        data = cursor.fetchall()
        return jsonify(data)

    finally:
        cursor.close()
        conn.close()
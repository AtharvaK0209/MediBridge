from flask import Blueprint, request, jsonify
from database import get_db_connection

ngo_bp = Blueprint("ngo", __name__)

@ngo_bp.route("/available-medicines")
def available_medicines():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM medicines
        WHERE status='SAFE' OR status='NEAR_EXPIRY'
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


@ngo_bp.route("/request-medicine", methods=["POST"])
def request_medicine():

    data = request.get_json()

    medicine_id = data.get("medicine_id")
    ngo_id = data.get("ngo_id")
    quantity = data.get("quantity")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ngo_id FROM ngo WHERE user_id=%s
    """, (ngo_id,))

    ngo = cursor.fetchone()

    if not ngo:
        return jsonify({"message": "NGO not found"}), 400

    ngo_id = ngo[0]

    cursor.execute("""
        INSERT INTO redistribution_requests
        (medicine_id, ngo_id, requested_quantity)
        VALUES (%s,%s,%s)
    """, (medicine_id, ngo_id, quantity))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Request sent"})

@ngo_bp.route("/ngo-stats/<int:user_id>")
def ngo_stats(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get NGO ID
    cursor.execute("SELECT ngo_id FROM ngo WHERE user_id=%s", (user_id,))
    ngo = cursor.fetchone()

    if not ngo:
        return jsonify({"message": "NGO not found"}), 400

    ngo_id = ngo["ngo_id"]

    # Total requests
    cursor.execute("""
        SELECT COUNT(*) AS total FROM redistribution_requests
        WHERE ngo_id=%s
    """, (ngo_id,))
    total = cursor.fetchone()["total"]

    # Approved requests
    cursor.execute("""
        SELECT COUNT(*) AS approved FROM redistribution_requests
        WHERE ngo_id=%s AND status='APPROVED'
    """, (ngo_id,))
    approved = cursor.fetchone()["approved"]

    cursor.close()
    conn.close()

    return jsonify({
        "total_requests": total,
        "approved_requests": approved
    })
import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="atharva@8956",
            database="expired_medicine_db"
        )
        return conn
    except Exception as e:
        print("Database Connection Error:", e)
        return None
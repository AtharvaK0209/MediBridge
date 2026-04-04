import mysql.connector
import os

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", "atharva@8956"),
            database=os.environ.get("DB_NAME", "expired_medicine_db")
        )
        return conn
    except mysql.connector.Error as e:
        print(f"[DB ERROR] {e}")
        return None
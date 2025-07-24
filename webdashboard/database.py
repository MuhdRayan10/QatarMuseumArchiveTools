from datetime import datetime
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def create_db():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS assets(
                         asset_id TEXT PRIMARY KEY,
                         user TEXT,   
                         month TEXT,
                         week INTEGER,
                         type TEXT)""")
    db.commit()
    db.close()

def add_asset(asset_id, user, month, week, data_type):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO assets values (?,?,?,?,?)", (asset_id, user, month, week, data_type))
        db.commit()  
        db.close()

    except sqlite3.IntegrityError:
        print(f"Asset with ID {asset_id} already exists.")

def get_counts(user=None):
    """Return aggregated counts, optionally filtered by user."""
    query = (
        "SELECT month, week,"
        " SUM(CASE WHEN type='images' THEN 1 ELSE 0 END) AS images,"
        " SUM(CASE WHEN type='videos' THEN 1 ELSE 0 END) AS videos,"
        " SUM(CASE WHEN type='audio' THEN 1 ELSE 0 END) AS audio,"
        " SUM(CASE WHEN type='documents' THEN 1 ELSE 0 END) AS documents"
        " FROM assets"
    )
    params = []
    if user:
        query += " WHERE user=?"
        params.append(user)
    query += " GROUP BY month, week"


    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()

    result = {}
    for row in rows:
        month = row["month"]
        week = row["week"]
        bucket = result.setdefault(month, {}).setdefault(
            week, {"images": 0, "videos": 0, "audio": 0, "documents": 0}
        )
        bucket["images"] += row["images"]
        bucket["videos"] += row["videos"]
        bucket["audio"] += row["audio"]
        bucket["documents"] += row["documents"]
    return {"all_data": result}

if __name__ == "__main__":
    create_db()
    add_asset("12345", "user1", "January", 1, "images")

    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM assets")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

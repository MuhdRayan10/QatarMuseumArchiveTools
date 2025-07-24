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

    cursor.execute("INSERT IGNORE INTO assets (?,?,?,?,?)", (asset_id, user, month, week, data_type))
    db.commit()    
    
if __name__ == "__main__":
    create_db()
    add_asset("12345", "user1", "January", 1, "images")

    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM assets")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

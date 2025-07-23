import sqlite3


def create_db():
    db = sqlite3.connect("./webdashboard/data.db")
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS asset_data(
                         user TEXT PRIMARY KEY,
                         month TEXT,
                         week INTEGER,
                         images INTEGER,
                         videos INTEGER,
                         audio INTEGER,
                         documents INTEGER)""")
    db.commit()
    db.close()

def add_asset(user, month, week, data_type):
    db = sqlite3.connect("./webdashboard/data.db")
    cursor = db.cursor()

    cursor.execute("SELECT DISTINCT user FROM asset_data")
    users = [u[0] for u in cursor.fetchall()]

    if user not in users:
        cursor.execute("INSERT INTO asset_data values(?,?,?,?,?,?,?)", (user, month, week, 0, 0, 0, 0))
        db.commit()

    cursor.execute(f"UPDATE asset_data SET {data_type}={data_type}+1 WHERE user= ?", (user,))
    db.commit()    
    
create_db()
add_asset('test_user', '10', 1, 'images') #increasing images count for test user

import sqlite3 as sql

def insertDetails(email, first, last, password, developer_id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO developer_details (developer_email, developer_firstName, developer_lastName, developer_password, developer_id) VALUES (?, ?, ?, ?, ?)", (email, first, last, password, developer_id))
        con.commit()
    except sql.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def checkCredentials(email, password):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM developer_details WHERE developer_email = ? AND developer_password = ?", (email, password))
        user = cur.fetchone()
        return user
    except sql.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

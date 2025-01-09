import sqlite3 as sql
import sqlite3

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

def checkCredentials(identifier, password):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM developer_details WHERE (developer_email = ? OR developer_id = ?) AND developer_password = ?", (identifier, identifier, password))
        user = cur.fetchone()
        return user
    except sql.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()


def insert_diary_entry(project_name, summary, programming_language, time_started, time_finished, description):
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diary_entry (project_name, summary, programming_language, time_started, time_finished, description) VALUES (?, ?, ?, ?, ?, ?)", (project_name, summary, programming_language, time_started, time_finished, description))
    conn.commit()
    conn.close()

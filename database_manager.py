import sqlite3 as sql
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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


def insert_diary_entry(developer_id, project_name, summary, programming_language, time_started, time_finished, description, date):
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diary_entry (developer_id, project_name, summary, programming_language, time_started, time_finished, description, date) VALUES (?, ?, ?, ?, ?, ?, ?,?)", (developer_id, project_name, summary, programming_language, time_started, time_finished, description, date))
    conn.commit()
    conn.close()

def get_all_diary_entries():
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diary_entry")
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_entries_by_developer_id(developer_id):
    try:
        conn = sqlite3.connect('database/data_source.db')
        cursor = conn.cursor()
        logger.debug(f"Executing query to fetch entries for developer_id: {developer_id}")
        cursor.execute('''
            SELECT * FROM diary_entry WHERE developer_id = ?
        ''', (developer_id,))
        entries = cursor.fetchall()
        logger.debug(f"Entries fetched: {entries}")
        conn.close()
        return entries
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return []
    except Exception as e:
        logger.error(f"Exception in get_entries_by_developer_id: {e}")
        return []
import sqlite3
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def insertDetails(email, first, last, password):
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO developer_details (developer_email, developer_firstName, developer_lastName, developer_password)
        VALUES (?, ?, ?, ?)
    ''', (email, first, last, password))
    conn.commit()
    conn.close()

def checkCredentials(email):
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT developer_email, developer_password, developer_firstName, developer_lastName FROM developer_details WHERE developer_email = ?
    ''', (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'developer_email': result[0],
            'developer_password': result[1],
            'developer_firstName': result[2],
            'developer_lastName': result[3]
        }
    return None

def get_user_details(email):
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT developer_firstName, developer_lastName, developer_email FROM developer_details WHERE developer_email = ?
    ''', (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'developer_firstName': result[0],
            'developer_lastName': result[1],
            'developer_email': result[2]
        }
    return None

# Adds diary entries into the database
def insert_diary_entry(developer_name, project_name, summary, programming_language, time_started, time_finished, description, date, developer_email, entry_timestamp):
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diary_entry (developer_name, project_name, summary, programming_language, time_started, time_finished, description, date, developer_email, entry_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (developer_name, project_name, summary, programming_language, time_started, time_finished, description, date, developer_email, entry_timestamp))
    conn.commit()
    conn.close()

# Retrieves all diary entries from the database filtered by developer_email
def get_diary_entries(developer_email):
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diary_entry WHERE developer_email = ?", (developer_email,))
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_all_diary_entries():
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diary_entry")
    entries = cursor.fetchall()
    conn.close()
    return entries

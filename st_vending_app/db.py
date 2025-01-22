# import sqlite3
# from config import DATABASE

# # Helper function to connect to SQLite DB
# def get_db_connection():
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# # Database setup function
# def init_db():
#     conn = get_db_connection()
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             mobile TEXT NOT NULL,
#             city TEXT NOT NULL,
#             area TEXT NOT NULL,
#             pin_code TEXT NOT NULL,
#             machine_id TEXT NOT NULL,
#             timestamp TEXT NOT NULL,
#             date TEXT NOT NULL,
#             unique_code TEXT,
#             collected INTEGER,
#             is_verify INTEGER DEFAULT 0,
#             otp TEXT
#         );
#     ''')
#     conn.commit()
#     conn.close()




import sqlite3
from config import DATABASE
import time
from datetime import datetime, timedelta



# Helper function to connect to SQLite DB
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Database setup function
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            city TEXT NOT NULL,
            area TEXT NOT NULL,
            pin_code TEXT NOT NULL,
            machine_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            updated_timestamp TEXT,
            updated_date TEXT,
            unique_code TEXT,
            collected_timestamp TEXT,
            collected_date TEXT,
            collected INTEGER,
            is_verify INTEGER DEFAULT 0,
            otp TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Insert record function
def insert_user(name, mobile, city, area, pin_code, machine_id, timestamp, date, unique_code=None, collected=None, is_verify=0, otp=None):
    conn = get_db_connection()
    
    # Insert user record into the database
    conn.execute('''
        INSERT INTO users (name, mobile, city, area, pin_code, machine_id, timestamp, date, unique_code, collected, is_verify, otp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', (name, mobile, city, area, pin_code, machine_id, timestamp, date, unique_code, collected, is_verify, otp))
    
    conn.commit()
    conn.close()


# Function to get a user record by mobile number
def get_user_by_mobile(mobile):
    conn = get_db_connection()
    cursor = conn.execute('''
        SELECT * FROM users WHERE mobile = ?;
    ''', (mobile,))
    user = cursor.fetchone()  # Fetch the first record matching the mobile number
    
    conn.close()
    
    if user:
        return dict(user)  # Convert the row to a dictionary for easier access
    else:
        return None  # Return None if no record is found
    

# Function to update records inserted 30 days ago
def reset_user_record():
    conn = get_db_connection()

    # Calculate the timestamp for 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d')

    # Update query for records inserted 30 days ago
    conn.execute('''
        UPDATE users
        SET unique_code = '', 
            collected_timestamp = ?, 
            collected_date = ?, 
            collected = 0
        WHERE collected_date <= ?;
    ''', ('', '', thirty_days_ago_str))

    conn.commit()
    conn.close()


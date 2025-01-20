import sqlite3
import streamlit as st
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio configuration from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')

# Database setup
DATABASE = 'items.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return items

def add_item(name):
    conn = get_db_connection()
    conn.execute('INSERT INTO items (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def update_item(item_id, name):
    conn = get_db_connection()
    conn.execute('UPDATE items SET name = ? WHERE id = ?', (name, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Send SMS with Twilio
def send_sms(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        st.success("SMS sent successfully!")
    except Exception as e:
        st.error(f"Failed to send SMS: {e}")

# Streamlit app layout
st.title("CRUD App with Streamlit")

# Initialize the database
init_db()

# Display items
st.header("Items List")
items = get_items()

for item in items:
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        new_name = st.text_input(f"Update item #{item['id']}", item['name'], key=f"update_{item['id']}")
    
    with col2:
        if st.button("Update", key=f"update_btn_{item['id']}"):
            if new_name.strip():
                update_item(item['id'], new_name)
                st.success(f"Updated item #{item['id']}")
            else:
                st.error("Item name cannot be empty.")
    
    with col3:
        if st.button("Delete", key=f"delete_btn_{item['id']}"):
            delete_item(item['id'])
            st.success(f"Deleted item #{item['id']}")

# Add new item section
st.header("Add New Item")
new_item = st.text_input("Item Name", "")

if st.button("Add Item"):
    if new_item.strip():
        add_item(new_item)
        st.success(f"Added item: {new_item}")
        
        # Send SMS notification about the new item
        message = f"New item added: {new_item}"
        send_sms(message)
    else:
        st.error("Item name cannot be empty.")

# Footer
st.text("CRUD operations with Streamlit and SQLite")

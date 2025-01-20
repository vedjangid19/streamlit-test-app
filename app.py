import sqlite3
import streamlit as st
from twilio.rest import Client
import os


# Access Twilio credentials from Streamlit secrets
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = st.secrets["TWILIO_PHONE_NUMBER"]
RECIPIENT_PHONE_NUMBER = st.secrets["RECIPIENT_PHONE_NUMBER"]

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
            name TEXT NOT NULL,
            homepage_id INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_items(homepage_id):
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items WHERE homepage_id = ?', (homepage_id,)).fetchall()
    conn.close()
    return items

def add_item(name, homepage_id):
    conn = get_db_connection()
    conn.execute('INSERT INTO items (name, homepage_id) VALUES (?, ?)', (name, homepage_id))
    conn.commit()
    conn.close()

def update_item(item_id, name, homepage_id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET name = ? WHERE id = ? AND homepage_id = ?', (name, item_id, homepage_id))
    conn.commit()
    conn.close()

def delete_item(item_id, homepage_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ? AND homepage_id = ?', (item_id, homepage_id))
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

# Function to handle homepage routing based on query parameters
def homepage_route(homepage_id):
    st.title(f"CRUD App for Homepage {homepage_id}")

    # Initialize the database
    init_db()

    # Display items for the current homepage
    st.header(f"Items List for Homepage {homepage_id}")
    items = get_items(homepage_id)

    for item in items:
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            new_name = st.text_input(f"Update item #{item['id']}", item['name'], key=f"update_{item['id']}")

        with col2:
            if st.button("Update", key=f"update_btn_{item['id']}"):
                if new_name.strip():
                    update_item(item['id'], new_name, homepage_id)
                    st.success(f"Updated item #{item['id']}")
                else:
                    st.error("Item name cannot be empty.")

        with col3:
            if st.button("Delete", key=f"delete_btn_{item['id']}"):
                delete_item(item['id'], homepage_id)
                st.success(f"Deleted item #{item['id']}")

    # Add new item section
    st.header("Add New Item")
    new_item = st.text_input("Item Name", "")

    if st.button("Add Item"):
        if new_item.strip():
            add_item(new_item, homepage_id)
            st.success(f"Added item: {new_item}")

            # Send SMS notification about the new item
            message = f"New item added: {new_item}"
            send_sms(message)
        else:
            st.error("Item name cannot be empty.")

# Main function to simulate the URL routing
def main():
    # Get query parameters from the URL
    query_params = st.query_params

    # Check if we have a valid homepage parameter
    if 'homepage' in query_params:
        try:
            homepage_id = int(query_params['homepage'][0])  # Get homepage ID from URL query parameter
            homepage_route(homepage_id)  # Show content based on homepage_id
        except ValueError:
            st.error("Invalid homepage number.")
    else:
        st.warning("Please select a homepage by adding ?homepage=<number> to the URL.")

# Run the app
if __name__ == "__main__":
    main()

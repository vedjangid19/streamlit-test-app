import random
from twilio.rest import Client
import streamlit as st


# Access Twilio credentials from Streamlit secrets
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = st.secrets["TWILIO_PHONE_NUMBER"]


# Generate a 4-digit OTP
def generate_otp():
    return random.randint(1000, 9999)

# Send OTP via SMS using Twilio API
def send_otp_sms(mobile, msg_body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        # body=f"Your OTP for vending machine: {otp}",
        body=msg_body,
        from_=TWILIO_PHONE_NUMBER,
        to=mobile
    )
    return message.sid

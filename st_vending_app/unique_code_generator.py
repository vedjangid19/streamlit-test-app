import random
import string
from datetime import datetime, timedelta

def generate_unique_code():
    # Generate a 6-digit unique code (you can change this logic if required)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def check_code_validity(code_timestamp):
    # Check if the unique code is still valid (valid for 30 days)
    current_time = datetime.now()
    code_time = datetime.strptime(code_timestamp, "%Y-%m-%d %H:%M:%S")
    return (current_time - code_time) <= timedelta(days=30)

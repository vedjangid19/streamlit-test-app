import streamlit as st
from db import get_db_connection, insert_user, get_user_by_mobile
from otp_service import generate_otp, send_otp_sms
from unique_code_generator import generate_unique_code
from datetime import datetime
from machine_dispatcher import notify_machine_to_dispatch

# Function to display Vending Form and OTP Verification
def vending_form():
    st.title("Vending Machine")
    st.header("Enter Your Details")

    # Collecting user details
    machine_id = st.text_input("Machine ID", "")
    name = st.text_input("Your Name", "")
    mobile = st.text_input("Mobile Number", "")
    city = st.text_input("City", "")
    area = st.text_input("Area", "")
    pin_code = st.text_input("PIN Code", "")

    if st.button("Submit"):
        if name and mobile and city and area and pin_code and machine_id:
            # Generate OTP and send SMS
            otp = generate_otp()
            msg_body = f"Your verification OTP for vending machine [ {machine_id} ]: {otp}"
            send_otp_sms(mobile, msg_body)

            # Insert user details into the database
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date = datetime.now().strftime("%Y-%m-%d")

            insert_user(
                name=name,
                mobile=mobile,
                city=city,
                area=area,
                pin_code=pin_code,
                machine_id=machine_id,
                timestamp=timestamp,
                date=date,
                otp=otp
            )

            # Store mobile and machine_id in session state
            st.session_state.mobile = mobile
            st.session_state.machine_id = machine_id

            st.success("OTP has been sent to your mobile. Please enter it below.")

            # OTP input field
            otp_input = st.text_input("Enter OTP", "", type="password")

            if otp_input:
                # Fetch the user record from the database by mobile number
                user_record = get_user_by_mobile(mobile)
                if user_record:
                    generated_otp = user_record['otp']

                    # Check if the entered OTP matches the generated OTP
                    if int(generated_otp) == int(otp_input):
                        # OTP verified successfully, generate unique code
                        unique_code = generate_unique_code()

                        # Update the database with the unique code
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute('''
                            UPDATE users
                            SET unique_code = ?, collected = ?, is_verify = ?
                            WHERE mobile = ? AND machine_id = ?;
                        ''', (unique_code, 0, 1, mobile, machine_id))
                        conn.commit()
                        conn.close()

                        machine_number = '+919769496162'
                        # Send the unique code via SMS
                        msg_body = f"OTP Verified. Here is your unique code for collection from machine {machine_id}: {unique_code}"
                        send_otp_sms(machine_number, msg_body)

                        st.success(f"OTP Verified! Your unique code for collection: {unique_code}")
                    else:
                        st.error("Invalid OTP. Please try again.")
                else:
                    st.error("User not found.")
        else:
            st.error("Please fill in all the fields.")

# Main function to run the Streamlit app
def main():
    if 'mobile' not in st.session_state or 'machine_id' not in st.session_state:
        st.warning("Please fill out the vending machine form to get started.")
        vending_form()
    else:
        # If session state exists, show the OTP verification part
        st.header("OTP Verification")
        otp_input = st.text_input("Enter OTP", "", type="password")

        if otp_input:
            mobile = st.session_state.mobile
            machine_id = st.session_state.machine_id

            # Fetch the user record from the database by mobile number
            user_record = get_user_by_mobile(mobile)
            if user_record:
                generated_otp = user_record['otp']

                # Check if the entered OTP matches the generated OTP
                if int(generated_otp) == int(otp_input):
                    # OTP verified successfully, generate unique code
                    unique_code = generate_unique_code()

                    # Update the database with the unique code
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE users
                        SET unique_code = ?, collected = ?, is_verify = ?
                        WHERE mobile = ? AND machine_id = ?;
                    ''', (unique_code, 0, 1, mobile, machine_id))
                    conn.commit()
                    conn.close()

                    # Send the unique code via SMS
                    msg_body = f"OTP Verified. Here is your unique code for collection from machine {machine_id}: {unique_code}"
                    send_otp_sms(mobile, msg_body)

                    st.success(f"OTP Verified! Your unique code for collection: {unique_code}")
                else:
                    st.error("Invalid OTP. Please try again.")
            else:
                st.error("User not found.")
        else:
            st.info("Please enter the OTP sent to your mobile.")

if __name__ == "__main__":
    main()

import streamlit as st
from email_validator import validate_email, EmailNotValidError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(page_title="Webinar Registration", layout="centered")
st.title("📋 Webinar Registration")

# Sample webinars
WEBINARS = [
    "Select a webinar...",
    "Python Basics for Beginners",
    "Advanced Web Development",
    "Data Science with Python",
    "Cloud Computing Essentials",
    "Machine Learning 101"
]

@st.cache_resource
def get_google_sheet():
    """Connect to Google Sheet"""
    try:
        # Check if running on Streamlit Cloud (secrets) or locally (service account file)
        if "google_service_account" in st.secrets:
            credentials_dict = st.secrets["google_service_account"]
        else:
            # For local development, use service account JSON file
            if os.path.exists("service_account.json"):
                with open("service_account.json") as f:
                    credentials_dict = json.load(f)
            else:
                st.error("❌ No Google credentials found. Please set up authentication.")
                return None
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(creds)
        
        # Open or create the spreadsheet
        try:
            sheet = client.open("Webinar Registrations").worksheet("Registrations")
        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet if it doesn't exist
            spreadsheet = client.create("Webinar Registrations")
            sheet = spreadsheet.add_worksheet("Registrations", rows=1000, cols=7)
            
            # Add headers
            headers = ["ID", "Webinar", "Email", "First Name", "Last Name", "Phone", "Registration Date"]
            sheet.append_row(headers)
        
        return sheet
    except Exception as e:
        st.error(f"❌ Error connecting to Google Sheets: {e}")
        return None

def validate_email_format(email):
    """Validate email format"""
    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone(phone):
    """Validate phone number (basic validation)"""
    phone_digits = re.sub(r'[\s\-\(\)\.]+', '', phone)
    
    if len(phone_digits) == 10 and phone_digits.isdigit():
        return True, ""
    elif len(phone_digits) == 11 and phone_digits.startswith('1') and phone_digits.isdigit():
        return True, ""
    else:
        return False, "Phone number must be 10 digits (or 11 with country code)"

def save_registration(sheet, webinar, email, first_name, last_name, phone):
    """Save registration to Google Sheet"""
    try:
        # Get all rows to find max ID
        all_rows = sheet.get_all_values()
        registration_id = len(all_rows)  # Row number will be our ID
        
        # Prepare the row
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [registration_id, webinar, email, first_name, last_name, phone, registration_date]
        
        # Append to sheet
        sheet.append_row(new_row)
        
        # Return the data as a dict
        return True, "Registration successful!", {
            'id': registration_id,
            'webinar': webinar,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'registration_date': registration_date
        }
    except gspread.exceptions.CellNotFound:
        return False, "Email already exists!", None
    except Exception as e:
        return False, f"Error saving registration: {e}", None

# Form creation
with st.form("registration_form"):
    st.subheader("Complete your registration below")
    
    webinar = st.selectbox(
        "Select a webinar",
        WEBINARS,
        help="Choose which webinar you'd like to attend"
    )
    
    email = st.text_input(
        "Email Address",
        placeholder="your.email@example.com",
        help="We'll send you confirmation details"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", placeholder="John")
    with col2:
        last_name = st.text_input("Last Name", placeholder="Doe")
    
    phone = st.text_input(
        "Phone Number",
        placeholder="(123) 456-7890",
        help="We may contact you with webinar details"
    )
    
    submitted = st.form_submit_button("Register for Webinar", use_container_width=True)

# Form validation and submission
if submitted:
    errors = []
    
    if webinar == "Select a webinar...":
        errors.append("❌ Please select a webinar")
    
    if not email:
        errors.append("❌ Email is required")
    else:
        is_valid, error_msg = validate_email_format(email)
        if not is_valid:
            errors.append(f"❌ Invalid email: {error_msg}")
    
    if not first_name:
        errors.append("❌ First name is required")
    
    if not last_name:
        errors.append("❌ Last name is required")
    
    if not phone:
        errors.append("❌ Phone number is required")
    else:
        is_valid, error_msg = validate_phone(phone)
        if not is_valid:
            errors.append(f"❌ {error_msg}")
    
    if errors:
        st.error("Please fix the following errors:")
        for error in errors:
            st.write(error)
    else:
        sheet = get_google_sheet()
        if sheet:
            success, message, registered_data = save_registration(sheet, webinar, email, first_name, last_name, phone)
            
            if success:
                st.success(f"✅ {message}")
                st.balloons()
                
                st.markdown("### 📋 Confirmation Details")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Registration ID", registered_data['id'])
                    st.metric("First Name", registered_data['first_name'])
                    st.metric("Last Name", registered_data['last_name'])
                
                with col2:
                    st.metric("Email", registered_data['email'])
                    st.metric("Phone", registered_data['phone'])
                
                st.info(f"**Webinar:** {registered_data['webinar']}")
                st.write(f"**Registration Date/Time:** {registered_data['registration_date']}")
                st.success("Your information has been securely stored in our database.")
            else:
                st.error(f"❌ {message}")
        else:
            st.error("❌ Could not connect to database")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    For technical support, contact: support@example.com
    </div>
    """,
    unsafe_allow_html=True
)

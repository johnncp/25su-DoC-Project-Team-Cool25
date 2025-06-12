import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import datetime

# Initialize sidebar
SideBarLinks()
AlwaysShowAtBottom()

st.title("Add New Daycare Location")

# API endpoint
API_URL = "http://web-api:4000/location/locations"

# Create a form for NGO details
with st.form("add_location_form"):
    st.subheader("Daycare Location Information")

    # Required fields
    daycare_name = st.text_input("Daycare Name *")
    city = st.text_input("City *")
    country = st.text_input("Country *" )

    # Form submission button
    submitted = st.form_submit_button("Add Location")

    if submitted:
        # Validate required fields
        if not all([daycare_name, city, country]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            ngo_data = {
                "daycare_name": daycare_name,
                "city": city,
                "country_code": country,
                "owner_id": st.session_state['user_id']
            }

            try:
                # Send POST request to API
                response = requests.post(API_URL, json=ngo_data)

                if response.status_code == 201:
                    st.success("Location added successfully!")
                    # Clear the form
                    st.rerun()
                else:
                    st.error(
                        f"Failed to add Location: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Add a button to return to the NGO Directory
if st.button("Return to Planning Page"):
    st.switch_page("pages/04_Business_Planner.py")

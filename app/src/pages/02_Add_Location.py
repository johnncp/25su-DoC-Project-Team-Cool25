import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import datetime

# Initialize sidebar
SideBarLinks()

st.title("Add New NGO")

# API endpoint
API_URL = "http://web-api:4000/location/addlocations"

# Create a form for NGO details
with st.form("add_location_form"):
    st.subheader("Daycare Location Information")

    # Required fields
    name = st.number_input("Daycare ID *")
    country = st.text_input("City *")
    founding_year = st.text_input("Country *" )
    focus_area = st.time_input("Opening Time *")
    website = st.time_input("Closing Time *")
    monthly_price = st.number_input("Monthly Price *")

    # Form submission button
    submitted = st.form_submit_button("Add NGO")

    if submitted:
        # Validate required fields
        if not all([name, country, founding_year, focus_area, website]):
            st.error("Please fill in all required fields marked with *")
        else:
            if isinstance(focus_area, datetime.timedelta):
                jsonifiable_time = (datetime.datetime.min + focus_area).time()
            else:
                jsonifiable_time = focus_area
            
            if isinstance(website, datetime.timedelta):
                jsonifiable_time2 = (datetime.datetime.min + website).time()
            else:
                jsonifiable_time2 = website
            
            departure_time = jsonifiable_time
            time_two = jsonifiable_time2


            # Prepare the data for API
            ngo_data = {
                "daycare_id": int(name),
                "opening_time": departure_time.isoformat(),
                "closing_time": time_two.isoformat(),
                "monthly_price": monthly_price,
                "city": country,
                "country_code": founding_year,
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
                        f"Failed to add NGO: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Add a button to return to the NGO Directory
if st.button("Return to Planning Page"):
    st.switch_page("pages/01_Business_Planner.py")

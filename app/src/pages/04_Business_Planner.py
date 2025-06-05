import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from streamlit_extras.app_logo import add_logo
import datetime

st.set_page_config(layout = 'wide')

## need to change name soon

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Daycare Owner, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

viewLocations = False
addLocation = False
col1, col2, col3 = st.columns(3)

with col3:
    if st.button('Add a new location', 
             type='primary',
             use_container_width=True):
      API_URL = "http://web-api:4000/location//locations"
      addLocation = True
      st.switch_page('pages/05_Add_Location.py')

with col2:
  if st.button('Research new locations', 
                type='primary',
              use_container_width=True):
      st.write("Feature coming soon!")

with col1: 
  if st.button('See current locations',
              type='primary',
              use_container_width=True):
    API_URL = "http://web-api:4000/location/locations"
    #might not work
    viewLocations = True

API_URL = "http://web-api:4000/location//locations"

response = requests.get(API_URL)
if response.status_code == 200:
    locations = response.json()
st.write(locations)    

# this is set up like this for formatting reasons
if viewLocations == True and viewLocations == False:
  try: 
    response = requests.get(API_URL)
    if response.status_code == 200:
        locations = response.json()
    
    # Display results count

    st.write(f"Found {len(locations)} Locations")

    # Create expandable rows for each NGO
    for loc in locations:
        with st.expander(f"{loc['Daycare ID']} ({loc['Daycare Name']})"):
            st.write("**Basic Information**")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**City:** {loc['City']}")
                st.write(f"**Monthly Price:** {loc['Monthly Price']}")
                st.write("**Hours**")
                st.write(f"**Opens:** [{loc['Opening Time']}]")
                st.write(f"**Closes:** [{loc['Closing Time']}]")

            with col2:
                st.write(f"**Country:** {loc['Country']}")
                # buttons to update stuff
                with st.popover("Update Price"):
                   newPrice = st.number_input("Update price", min_value=0, max_value=1000, key=f"price_input_{loc['Daycare ID']}")
                st.write("\n\n")
                with st.popover("Update Opening Time"):
                   newOpen = st.time_input("Set new opening time for", value=loc['Opening Time'])
                with st.popover("Update Closing Time"):
                   newOpen = st.time_input("Set new closing time for", value=loc['Closing Time'])

  except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running on http://web-api:4000")
daycare_id = 0

#currently this does nothing
if addLocation == True:
    with st.form("add_location_form"):
        st.subheader("Daycare Location Information")

        # Required fields
        daycare_id = st.number_input("Daycare ID *")
        opening_time = st.time_input("Opening Time *")
        closing_time = st.time_input("Closing Time *")
        monthly_price = st.number_input("Monthly Price *")
        city = st.text_input("City *")
        country_code = st.text_input("Country Code *")

        # Form submission button
        submitted = st.form_submit_button("Add Location")



        if submitted:
            # Validate required fields
            if not all([daycare_id, opening_time, closing_time, monthly_price, city, country_code]):
                st.error("Please fill in all required fields marked with *")
            else:
                # Prepare the data for API
                location_data = {
                    "Daycare ID": int(daycare_id),
                    "Opening Time": opening_time,
                    "Closing Time": closing_time,
                    "Monthly Price": monthly_price,
                    "Country Code": country_code,
                }

                try:
                    # Send POST request to API
                    response = requests.post(API_URL, json=location_data)

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

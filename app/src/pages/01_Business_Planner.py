import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from streamlit_extras.app_logo import add_logo

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Daycare Owner, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

col1, col2, col3 = st.columns(3)

with col3:
    if st.button('Add a new location', 
             type='primary',
             use_container_width=True):
      st.switch_page('pages/01_World_Bank_Viz.py')

with col2:
  if st.button('Research new locations', 
              type='primary',
              use_container_width=True):
    writer = True

viewLocations = False

with col1: 
  if st.button('See current locations',
              type='primary',
              use_container_width=True):
    API_URL = "http://web-api:4000/location/locations"
    #might not work
    viewLocations = True

# this is set up like this for formatting reasons
if viewLocations == True:
  try: 
    response = requests.get(API_URL)
    if response.status_code == 200:
        locations = response.json()
    
    # Display results count

    st.write(f"Found {len(locations)} Locations")

    # Create expandable rows for each NGO
    for loc in locations:
        with st.expander(f"{loc['Daycare ID']} ({loc['Country']})"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Basic Information**")
                st.write(f"**Country:** {loc['Country']}")
                st.write(f"**City:** {loc['City']}")
                st.write(f"**Monthly Price:** {loc['Monthly Price']}")

            with col2:
                st.write("**Hours**")
                st.write(f"**Opening:** [{loc['Opening Time']}]")

                      # Add a button to view full profile
                      #if st.button(f"View Full Profile", key=f"view_{loc['daycare_id']}"):
                          #st.session_state["selected_ngo_id"] = loc["daycare_id"]
                          #st.switch_page("pages/16_NGO_Profile.py")


  except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running on http://web-api:4000")
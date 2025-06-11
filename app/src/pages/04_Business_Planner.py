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
    try: 
      response = requests.get(API_URL)
      if response.status_code == 200:
        locations = response.json()

      st.write(f"Found {len(locations)} Locations")
      logger.info("Before the for loop")
      for loc in locations:
         logger.info(f"location = {loc}")
         with st.container(border = True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(loc['daycare_name'])
            with col2: 
               if st.button('View Full Profile', key=loc['daycare_id']):
                  st.session_state['selected_daycare_id'] = loc['daycare_id']
                  logger.info(f"session state = {st.session_state}")
                  st.switch_page('pages/06_Daycare_Profile.py')


    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running on http://web-api:4000")



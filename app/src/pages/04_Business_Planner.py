import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import requests
from streamlit_extras.app_logo import add_logo
import datetime

if st.session_state.get("go_to_daycare_profile"):
    logger.info("in the if true stmt")
    st.session_state["go_to_daycare_profile"] = False
    st.switch_page("pages/06_Daycare_Profile.py")
else:
    logger.info("in the else")
    logger.info(st.session_state)

st.set_page_config(layout="wide")

## need to change name soon

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks(),
AlwaysShowAtBottom()

st.title(f"Welcome Daycare Owner, {st.session_state['first_name']}.")
st.write("")
st.write("#### What would you like to do today?")
st.write("")

viewLocations = st.session_state.get('view_locations', False)
addLocation = False
col1, col2 = st.columns([2,1])



with col2:
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    if st.button("Research new locations", type="primary", use_container_width=True):
        st.switch_page("pages/07_Daycare_Research.py")
    if st.button("Add a new location", type="primary", use_container_width=True):
        API_URL = "http://web-api:4000/location/locations"
        st.switch_page("pages/05_Add_Location.py")

with col1:
    #if st.button("See current locations", type="primary", use_container_width=True):
        #st.session_state['view_locations'] = True
        #st.rerun()
        st.write("### View Current Locations Below: ")
        viewLocations = True

        if viewLocations:
            API_URL = "http://web-api:4000/location/locations"
            try:
                response = requests.get(API_URL)
                if response.status_code == 200:
                    locations = response.json()

                logger.info("Before the for loop")
                owner = st.session_state.get('user_id')
                filtered_locations = [loc for loc in locations if loc["owner_id"] == owner]
                st.write(f"Found {len(filtered_locations)} Locations")


                for loc in filtered_locations :
                    logger.info(f"location = {loc}")
                    with st.container(border=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(loc["daycare_name"])
                        with col2:
                            if st.button(
                                f'View Full Profile',
                                key=loc["daycare_id"],
                            ):
                                logger.info("in the button execution...")
                                st.session_state["selected_daycare_id"] = loc["daycare_id"]
                                st.session_state["go_to_daycare_profile"] = True
                                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running on http://web-api:4000")
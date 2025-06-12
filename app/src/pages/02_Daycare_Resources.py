import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import streamlit as st
import requests

logger = logging.getLogger(__name__)


st.set_page_config(page_title="Daycare Finder", layout="wide")

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

if st.session_state.get("go_to_daycare_profile"):
    st.session_state["go_to_daycare_profile"] = False
    st.switch_page("pages/06_Daycare_Profile.py")
else:
    logger.info("in the else")
    logger.info(st.session_state)

# set the title of the page
st.title('Find Daycares')
tab1, tab2 = st.tabs(["Search for Daycares", "Compare Daycares"])
viewLocations = st.session_state.get('view_locations', False)


with tab1:
    # User inputs
    
    country = st.text_input("Country Code", "BE")
    city = st.text_input("City", "Brussels")


    if viewLocations:
            try:
                params = {
                    "country_code": country,
                    "city": city
                }
                response = requests.get("http://web-api:4000/location/locations", params=params)
                if response.status_code == 200:
                    data = response.json()

                logger.info("Before the for loop")
                st.success(f"Found {len(data)} results")

                for item in data :
                    logger.info(f"location = {item}")
                    with st.container(border=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(item["daycare_name"])
                        with col2:
                            if st.button(
                                f'View Full Profile',
                                key=item["daycare_id"],
                            ):
                                logger.info("in the button execution...")
                                st.session_state["selected_daycare_id"] = item["daycare_id"]
                                st.session_state["go_to_daycare_profile"] = True
                                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running on http://web-api:4000")
if st.session_state.get("go_to_daycare_profile") == True:
    st.switch_page("pages/06_Daycare_Profile.py")


with tab2:
    selected_country = st.selectbox('Pick a country', ('BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY',
            'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE'))
    
    response = requests.get("http://web-api:4000/location/locations", params={"country_code": selected_country})
    if response.status_code == 200:
        data = response.json()
        if not data:
            st.warning("No daycares found for this country.")
    daycareNames = []
    daycareIds = []
    for item in data:
        daycareNames.append(item['daycare_name'])
        daycareIds.append(item["daycare_id"])

    if len(daycareNames) <= 1:
        st.write("##### Not enough daycares. Choose a different country")

    daycare1 = st.selectbox("Select first daycare", daycareNames, key="d1")
    st.write(daycareNames.index(daycare1))
    id1 = daycareIds[daycareNames.index(daycare1)]
    daycare2 = st.selectbox("Select second daycare", [d for d in daycareNames if d != daycare1], key="d2")
    if pd.notnull(daycare2): 
        id2 = daycareIds[daycareNames.index(daycare2)]

    if st.button("Compare!"): 
        col1, col2 = st.columns(2)

        with col1: 
            with st.container(border=True):
                try: 
                    response = requests.get(f"http://web-api:4000/location/locations/{id1}", params={"year": 2025})
                    if response.status_code == 200:
                        loc = response.json()

                        
                        st.subheader(loc["daycare_name"])
                        st.write(f"City: {loc['city']}")
                        st.write(f"Country: {loc['country_code']}")

                        # Display data
                        if loc.get("data"):
                            st.subheader("Data This Year")
                            for data in loc["data"]: 
                                    st.write(f"**Enrollment:** {data['Enrollment']}")
                                    st.write(f"**Monthly Price:** {data['Monthly Price']}")
                                    st.write(f"**Opening Time:** {data['Opening Time']}")
                                    st.write(f"**Closing Time:** {data['Closing Time']}")
                                    
                        else:
                            st.info("No data found for this location")

                
                except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the API: {str(e)}")
        with col2: 
            with st.container(border=True):
                try: 
                    response = requests.get(f"http://web-api:4000/location/locations/{id2}", params={"year": 2025})
                    if response.status_code == 200:
                        loc = response.json()

                        
                        st.subheader(loc["daycare_name"])
                        st.write(f"City: {loc['city']}")
                        st.write(f"Country: {loc['country_code']}")

                        # Display data
                        if loc.get("data"):
                            st.subheader("Data This Year")
                            for data in loc["data"]: 
                                    st.write(f"**Enrollment:** {data['Enrollment']}")
                                    st.write(f"**Monthly Price:** {data['Monthly Price']}")
                                    st.write(f"**Opening Time:** {data['Opening Time']}")
                                    st.write(f"**Closing Time:** {data['Closing Time']}")
                                    
                        else:
                            st.info("No data found for this location")

                
                except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the API: {str(e)}")

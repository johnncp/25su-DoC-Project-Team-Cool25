import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back
import streamlit as st
import requests
import time
import base64

logger = logging.getLogger(__name__)


st.set_page_config(page_title="Daycare Finder", layout="wide")

Back("10_Parent_Home.py")

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def fetch_users_by_role(role_id):
    try:
        response = requests.get(f"http://web-api:4000/users/role/{role_id}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching users: {e}")

background_img = get_base64("assets/Feature_background.png")

st.markdown(f"""
    <style>
    @keyframes fadeIn {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}

    .overlay-text {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-100%, -80%);
        color: #31333E;
        font-size: 3.8rem;
        font-weight: bold;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        padding: 15px 25px;
        border-radius: 8px;
        line-height: 0.8;
        opacity: 0;
        animation: fadeIn 0.5s ease-out forwards;
    }}
    </style>

    <img src="data:image/png;base64,{background_img}">
    <div class="overlay-text">🔎 Daycare Finder</div>
""", unsafe_allow_html=True)


# COUNTRY MAPPING
country_map = {
    'EU27_2020': 'European Union (27)',
    'BE': 'Belgium', 'BG': 'Bulgaria', 'CZ': 'Czechia', 'DK': 'Denmark',
    'DE': 'Germany', 'EE': 'Estonia', 'IE': 'Ireland', 'EL': 'Greece',
    'ES': 'Spain', 'FR': 'France', 'HR': 'Croatia', 'IT': 'Italy',
    'CY': 'Cyprus', 'LV': 'Latvia', 'LT': 'Lithuania', 'LU': 'Luxembourg',
    'HU': 'Hungary', 'MT': 'Malta', 'NL': 'Netherlands', 'AT': 'Austria',
    'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SI': 'Slovenia',
    'SK': 'Slovakia', 'FI': 'Finland', 'SE': 'Sweden'
}

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()
AlwaysShowAtBottom()

if st.session_state.get("go_to_daycare_profile"):
    st.session_state["go_to_daycare_profile"] = False
    st.switch_page("pages/06_Daycare_Profile.py")
else:
    logger.info("in the else")
    logger.info(st.session_state)


tab1, tab2 = st.tabs(["⊚ Search for Daycares", "⏀ Compare Domestic Daycares"])
viewLocations = st.session_state.get('view_locations', False)

@st.cache_data
def get_cities_for_country(country_code):
    """Fetch all unique cities for a given country code"""
    try:
        response = requests.get("http://web-api:4000/location/locations", 
                              params={"country_code": country_code})
        if response.status_code == 200:
            data = response.json()
            # Extract unique cities
            cities = sorted(list(set(item["city"] for item in data if item.get("city"))))
            return cities
        return []
    except:
        return []

with tab1:
    # Country selection dropdown
    country_codes = sorted(country_map.keys())
    country_names = [f"{country_map[code]} ({code})" for code in country_codes]

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.selected_country_display = st.selectbox("Select Country", country_names)
        # Extract country code from the display name
        st.session_state.selected_country = st.session_state.selected_country_display.split(" (")[-1].rstrip(")")
    
    # City selection dropdown - filtered based on selected country
    with col2:
        cities = get_cities_for_country(st.session_state.selected_country)
        if cities:
            st.session_state.selected_city = st.selectbox("Select City", cities)
        else:
            st.warning(f"No cities found for {country_map[st.session_state.selected_country]}. Try another country.")
            st.session_state.selected_city = None

    # Search button
    if st.session_state.selected_city:
        params = {
            "country_code": st.session_state.selected_country,
            "city": st.session_state.selected_city
        }
        response = requests.get("http://web-api:4000/location/locations", params=params)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Found {len(data)} results.")

            # Create grid layout with 3 columns
            for i in range(0, len(data), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(data):
                        item = data[i + j]
                        with cols[j]:
                            with st.container(border=True):
                                st.subheader(item["daycare_name"])
                                st.write(f"{item['city']}, {country_map.get(item['country_code'], item['country_code'])}")
                                
                                if st.button("View Details", 
                                           type='primary', 
                                           use_container_width=True, 
                                           key=f"view_{item['daycare_id']}"):
                                    st.session_state['selected_daycare_id'] = item['daycare_id']
                                    st.switch_page("pages/18_Parent_Daycare_Profile.py")
        else:
            st.error("Failed to fetch locations")

with tab2:
    country_codes_tab2 = sorted(country_map.keys())
    country_names_tab2 = [f"{country_map[code]} ({code})" for code in country_codes_tab2]
    
    selected_country_display_tab2 = st.selectbox('Pick a country', country_names_tab2, key="country_tab2")
    selected_country = selected_country_display_tab2.split(" (")[-1].rstrip(")")
    
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

    col1, col2 = st.columns(2)
    with col1:
        daycare1 = st.selectbox("Select first daycare", daycareNames, key="d1")
        id1 = daycareIds[daycareNames.index(daycare1)]
    with col2:
        daycare2 = st.selectbox("Select second daycare", [d for d in daycareNames if d != daycare1], key="d2")
        if pd.notnull(daycare2): 
            id2 = daycareIds[daycareNames.index(daycare2)]

    if st.button("Compare Daycares", use_container_width=True, type="primary"): 
        st.divider()

        with st.spinner("Goo goo gaa gaa..."):
            time.sleep(1.6)
        
        st.balloons()
        
        col1, col2 = st.columns(2)

        with col1: 
            with st.container(border=True):
                try: 
                    response = requests.get(f"http://web-api:4000/location/locations/{id1}", params={"year": 2025})
                    if response.status_code == 200:
                        loc = response.json()

                        
                        st.header(loc["daycare_name"])
                        st.write(f"{loc['city']}, {country_map.get(item['country_code'], item['country_code'])}")

                        # Display data
                        if loc.get("data"):
                            st.subheader("Details")
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

                        
                        st.header(loc["daycare_name"])
                        st.write(f"{loc['city']}, {country_map.get(item['country_code'], item['country_code'])}")

                        # Display data
                        if loc.get("data"):
                            st.subheader("Details")
                            for data in loc["data"]: 
                                    st.write(f"**Enrollment:** {data['Enrollment']}")
                                    st.write(f"**Monthly Price:** {data['Monthly Price']}")
                                    st.write(f"**Opening Time:** {data['Opening Time']}")
                                    st.write(f"**Closing Time:** {data['Closing Time']}")
                                    
                        else:
                            st.info("No data found for this location")

                
                except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the API: {str(e)}")
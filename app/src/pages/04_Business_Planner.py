import logging
import streamlit as st
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back
import requests
from streamlit_extras.app_logo import add_logo
import datetime, base64

st.set_page_config(layout="wide")

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

logger = logging.getLogger(__name__)

if st.session_state.get("go_to_daycare_profile"):
    logger.info("in the if true stmt")
    st.session_state["go_to_daycare_profile"] = False
    st.switch_page("pages/06_Daycare_Profile.py")
else:
    logger.info("in the else")
    logger.info(st.session_state)

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
AlwaysShowAtBottom()

Back("00_Daycare_Home.py")

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
    <div class="overlay-text">☰ Business Planner</div>
""", unsafe_allow_html=True)

viewLocations = st.session_state.get('view_locations', False)
addLocation = False
col1, col2 = st.columns([2,1])



with col2:
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
        st.header("View Current Locations Below: ")
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
                st.success(f"Retrieved {len(filtered_locations)} Locations")


                for loc in filtered_locations :
                    logger.info(f"location = {loc}")
                    with st.container(border=True):
                        col1, col2 = st.columns([3,.2])
                        with col1:
                            st.subheader(loc["daycare_name"])
                            st.write(f"{loc['city']}, {country_map.get(loc['country_code'], loc['country_code'])}")
                        with col2:
                            if st.button(
                                f'→',
                                key=loc["daycare_id"],
                            ):
                                logger.info("in the button execution...")
                                st.session_state["selected_daycare_id"] = loc["daycare_id"]
                                st.session_state["go_to_daycare_profile"] = True
                                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running on http://web-api:4000")
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import logging, base64

# Initialize sidebar
SideBarLinks()

logger = logging.getLogger(__name__)

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
    <div class="overlay-text">☰ Discover Affinity Groups</div>
""", unsafe_allow_html=True)

st.markdown("The place to unearth *your* community.")


# Country code to full name
country_map = {
    'EU27_2020': 'European Union (27)',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CZ': 'Czechia',
    'DK': 'Denmark',
    'DE': 'Germany',
    'EE': 'Estonia',
    'IE': 'Ireland',
    'EL': 'Greece',
    'ES': 'Spain',
    'FR': 'France',
    'HR': 'Croatia',
    'IT': 'Italy',
    'CY': 'Cyprus',
    'LV': 'Latvia',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'HU': 'Hungary',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'AT': 'Austria',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'FI': 'Finland',
    'SE': 'Sweden'
}

# Full name to country code
name_to_code = {v: k for k, v in country_map.items()}

# API endpoint
API_URL = "http://web-api:4000/group/groups"

# Create filter columns
col1, col2, col3 = st.columns(3)

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        groups = response.json()

        # Extract unique values for filters
        countries = sorted(list(set(group["country_code"] for group in groups)))
        focus_area = sorted(list(set(group["focus_area"] for group in groups)))
        resource_type = sorted(list(set(group["resource_type"] for group in groups)))

        # Create filters
        # Use full country names
        country_codes = set(group["country_code"] for group in groups)
        country_names = sorted([country_map.get(code, code) for code in country_codes])

        # Select full country name
        with st.sidebar:
            selected_country_name = st.selectbox("Filter by Country", ["All"] + country_names)
            selected_focus = st.selectbox("Filter by Focus Area", ["All"] + focus_area)
            selected_type = st.selectbox("Filter by Resource Type", ["All"] + resource_type)

        # Build query parameters
        params = {}
        if selected_country_name != "All":
            country_code = name_to_code.get(selected_country_name)
            if country_code:
                params["country_code"] = country_code
        if selected_focus != "All":
            params["focus_area"] = selected_focus
        if selected_type != "All":
            params["resource_type"] = selected_type

        # Get filtered data
        filtered_response = requests.get(API_URL, params=params)
        if filtered_response.status_code == 200:
            filtered_groups = filtered_response.json()

            # Display results count

            col1, col2 = st.columns(2)
            with col1:
                st.info("← Find your place with specific filters on the sidebar.")
            with col2:
                if len(filtered_groups) > 0:
                    st.success(f"Found {len(filtered_groups)} Resources.")
                else:
                    st.warning(f"Found {len(filtered_groups)} Resources. We recommend expanding your criteria.")
            
            st.divider()

            # Create 3-column grid layout
            for i in range(0, len(filtered_groups), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(filtered_groups):
                        group = filtered_groups[i + j]
                        country_full = country_map.get(group['country_code'], group['country_code'])
                        
                        with cols[j]:
                            with st.expander(f"{group['resource_name']} ({group['city']}, {group['country_code']})"):
                                st.write("**Basic Information**")
                                st.write(f"**Resource Type:** {group['resource_type']}")
                                st.write(f"**Focus Area:** {group['focus_area']}")
                                st.write(f"**Description:** {group['description']}")
                                
                                st.divider()
                                
                                st.write(f"**City:** {group['city']}")
                                st.write(f"**Country:** {country_full}")
                                st.write(f"**Website:** [{group['website']}]({group['website']})")

                                # Add a button to view full profile
                                #if st.button(f"View Full Profile", key=f"view_{group['NGO_ID']}"):
                                   # st.session_state["selected_ngo_id"] = group["NGO_ID"]
                                  # st.switch_page("pages/16_NGO_Profile.py")

    else:
        st.error("Failed to fetch Resource data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")

st.sidebar.divider()
AlwaysShowAtBottom()
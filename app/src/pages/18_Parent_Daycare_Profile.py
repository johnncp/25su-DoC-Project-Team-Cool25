import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom

# Initialize sidebar
SideBarLinks()
AlwaysShowAtBottom()

st.title("Daycare Profile")

# Get NGO ID from session state
location_id = st.session_state.get("selected_daycare_id")

if location_id is None:
    st.error("No Location selected")
    st.button(
        "Return to Business Planning Page",
        on_click=lambda: st.switch_page("pages/04_Business_Planner.py"),
    )
else:
    # API endpoint
    API_URL = f"http://web-api:4000/location/locations/{location_id}"

    try:
        # Fetch NGO details
        response = requests.get(API_URL)

        if response.status_code == 200:
            loc = response.json()

            # Display basic information
            st.header(loc["daycare_name"])

            st.subheader("Basic Information")
            st.write("\n\n")

            st.write(f"**City:** {loc['city']}")
            st.write(f"**Country:** {loc['country_code']}")

            # Display data
            if loc.get("data"):
                for data in loc["data"]:
                    if data["Year"] == 2025: 
                        st.write(f"**Enrollment:** {data['Enrollment']}")
                        st.write(f"**Monthly Price:** {data['Monthly Price']}")
                        st.write(f"**Opening Time:** {data['Opening Time']}")
                        st.write(f"**Closing Time:** {data['Closing Time']}")
                        
            else:
                st.info("No data found for this location")


        elif response.status_code == 404:
            st.error("Location not found")
        else:
            st.error(
                f"Error fetching DaycareLocation data: {response.json().get('error', 'Unknown error')}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")

# Add a button to return to the NGO Directory
st.write("\n\n")
if st.button("Return to Daycare Finder"):
    # Clear the selected NGO ID from session state
    if "selected_daycare_id" in st.session_state:
        del st.session_state["selected_daycare_id"]
    st.switch_page("pages/02_Daycare_Resources.py")

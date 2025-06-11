import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Resource Directory")

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
        with col1:
            selected_country = st.selectbox("Filter by Country", ["All"] + countries)

        with col2:
            selected_focus = st.selectbox("Filter by Focus Area", ["All"] + focus_area)

        with col3:
            selected_type = st.selectbox("Filter by Resource Type", ["All"] + resource_type,)

        # Build query parameters
        params = {}
        if selected_country != "All":
            params["country_code"] = selected_country
        if selected_focus != "All":
            params["focus_area"] = selected_focus
        if selected_type != "All":
            params["resource_type"] = selected_type

        # Get filtered data
        filtered_response = requests.get(API_URL, params=params)
        if filtered_response.status_code == 200:
            filtered_groups = filtered_response.json()

            # Display results count
            st.write(f"Found {len(filtered_groups)} Resources")

            # Create expandable rows for each NGO
            for group in filtered_groups:
                with st.expander(f"{group['resource_name']} ({group['country_code']})"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Basic Information**")
                        st.write(f"**Resource Type:** {group['resource_type']}")
                        st.write(f"**Focus Area:** {group['focus_area']}")
                        st.write(f"**Description:** {group['description']}")


                    with col2:
                        #st.write("**Contact Information**")
                        st.write(f"**City:** {group['city']}")
                        st.write(f"**Country:** {group['country_code']}")


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

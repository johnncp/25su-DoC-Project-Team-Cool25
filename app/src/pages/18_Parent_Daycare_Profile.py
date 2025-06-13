import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back

# Initialize sidebar
SideBarLinks()
AlwaysShowAtBottom()

Back("12_Parent_Daycare_Resources.py")

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
            st.title(loc["daycare_name"])
            st.write(f"{loc['city']}, {country_map.get(loc['country_code'], loc['country_code'])}")

            st.subheader("Details")
            st.write("\n\n")

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

st.divider()

API_KEY = 'b7fbb637b8044d34b684ae6076ee98e2'
DEFAULT_TOPIC = f"{loc['city']}, {country_map.get(loc['country_code'], loc['country_code'])}"
user_topic = DEFAULT_TOPIC

# Display
st.header(f"The Latest on {user_topic}")

# Text input from user
user_topic = st.text_input("Or click to refine queries yourself:", value=DEFAULT_TOPIC)

# Disclaimer
st.caption("• Eurobébé is not affiliated with the following articles and does not confirm factuality. Use intended for informational purposes only.")

# Request to NewsAPI
url = f"https://newsapi.org/v2/everything?q={user_topic}&sortBy=publishedAt&language=en&apiKey={API_KEY}"

# Fetch
response = requests.get(url)
data = response.json()

if data.get("articles"):
    articles = data["articles"][:6]  # Top 3

    # Create 3 columns
    cols = st.columns(3)

    for i, article in enumerate(articles):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:10px; background-color:#F4F4F4;">
                    <img src="{article['urlToImage']}" style="width:100%; border-radius:8px; margin-bottom:10px;" />
                    <h4 style="margin-top:0;">{article['title']}</h4>
                    <p>{article['description'] or ''}</p>
                    <a href="{article['url']}" target="_blank">Read more</a>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning("No articles found. Try a different topic.")
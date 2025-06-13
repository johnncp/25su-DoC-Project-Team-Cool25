import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back


# Initialize sidebar
Back("04_Business_Planner.py")
SideBarLinks()
AlwaysShowAtBottom()

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

# Get ID from session state
location_id = st.session_state.get("selected_daycare_id")

if "show_inputs" not in st.session_state:
        st.session_state['show_inputs'] = False
if "update_location_data" not in st.session_state:
        st.session_state['update_location_data'] = False
if "delete_location" not in st.session_state:
        st.session_state['delete_location'] = False


col1, col2, col3 = st.columns([3, 0.2, 1])

with col1: 
    if location_id is None:
        st.error("No Location selected")
        st.button(
            "Return to Business Planning Page",
            on_click=lambda: st.switch_page("pages/04_Business_Planner.py"),
        )
    else:
        API_URL = f"http://web-api:4000/location/locations/{location_id}"

        try:
            response = requests.get(API_URL)

            if response.status_code == 200:
                loc = response.json()

                # Display basic information
                st.title(loc["daycare_name"])
                st.header("Location")
                st.write(f"{loc['city']}, {country_map.get(loc['country_code'], loc['country_code'])}")

                
                # Display data
                if loc.get("data"):
                        st.header("Data Over the Years")
                        selected_year = st.selectbox("Choose a year", (2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015))
                        st.divider()
                        for data in loc["data"]:
                            if data["Year"] == selected_year: 
                                st.write("\n\n")
                                st.write(f"**Enrollment:** {data['Enrollment']}")
                                st.write(f"**Monthly Price:** {data['Monthly Price']}")
                                budget = float(data["Monthly Budget"]) if data["Monthly Budget"] else 0.0
                                st.write(f"**Monthly Budget:** ${budget:,.2f}")
                                percent = float(data["Percent Budget Used"]) if data["Percent Budget Used"] else 0.0
                                st.write(f"**Percent of Budget Used:** {percent:,.2f}%")
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

# creates update location inputs on page
with col3: 
    if selected_year == 2025:
        for _ in range(19):
            st.write("\n\n")

                        
        if st.button("Update Location Details"):
            st.session_state['show_inputs'] = not st.session_state['show_inputs']

        if st.session_state['show_inputs']:
            cola, colb = st.columns(2)

            with cola: 
                enrollment = st.number_input("Update Enrollment", value=None, placeholder="Enter a number")
                monthly_price = st.number_input("Update Monthly Price", value=None, placeholder="Enter a number")
                opening = st.time_input("Update Opening Time", value=None)
                if st.button("Submit"): 
                    st.write("ugh")
                    st.session_state["update_location_data"] = not st.session_state["update_location_data"]

            with colb: 
                monthly_budget = st.number_input("Update Monthly Budget", value=None, placeholder="Enter a number")
                percent_used = st.number_input("Update Percent of Budget Used", value=None, placeholder="Enter a number")                
                closing = st.time_input("Update Closing Time", value=None)

# this should be the put request to update the daycare location data
if st.session_state["update_location_data"]: 

            payload = {
                "enrollment": enrollment,
                "monthly_price": monthly_price,
                "monthly_budget": monthly_budget,
                "percent_budget_used": percent_used,
                "opening_time": opening.strftime("%H:%M:%S") if opening else None,
                "closing_time": closing.strftime("%H:%M:%S") if closing else None,
                "year": 2025
            }

            try:
                response1 = requests.put(f"http://web-api:4000/daycaredata/data/{location_id}",json=payload)

                if response1.status_code == 200:
                    st.success("Data updated successfully!")

                    st.session_state['show_inputs'] = not st.session_state['show_inputs']
                    st.session_state['update_location_data'] = not st.session_state['update_location_data']

                    st.rerun()
                else:
                    st.error(f"Failed to update data: {response1.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")


# add button to delete daycare
if st.button("Delete Daycare"):
     col1, col2, col3 = st.columns([0.5,0.5,0.5])
     st.session_state['delete_location'] = not st.session_state['delete_location']
    
if st.session_state['delete_location']:
            st.error("Are you sure you want to delete this location?")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Yes, delete"):
                    st.session_state["confirm_delete"] = True

            with col2:
                if st.button("Cancel"):
                    st.session_state["delete_location"] = False
                    st.rerun()


# if user wants to delete the location
if st.session_state.get("confirm_delete"):
    try:
        response2 = requests.delete(f"http://web-api:4000/location/locations/{location_id}")

        if response2.status_code == 200:
            st.success("Data updated successfully!")

            #reset the session states
            del st.session_state["confirm_delete"]
            if "delete_location" in st.session_state:
                del st.session_state["delete_location"]
            if "selected_daycare_id" in st.session_state:
                del st.session_state["selected_daycare_id"]

            st.switch_page("pages/04_Business_Planner.py")
        else:
                    st.error(f"Failed to update data: {response2.text}")

    except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")

st.divider()

API_KEY = 'a6025c9e68c4420e8eecb10dd38480da'
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
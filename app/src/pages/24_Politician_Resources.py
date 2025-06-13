import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back
import requests
import plotly.express as px
import base64, logging

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
        transform: translate(-125%, -80%);
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
    <div class="overlay-text">📁 Resources</div>
""", unsafe_allow_html=True)


SideBarLinks()
AlwaysShowAtBottom()

st.write("Get a clear picture of life across Europe — from how many hours people work each week, " \
"to how prices are changing, and how much governments are investing in family support.")

st.divider()


API_URL = "http://web-api:4000/hours/weeklyhours"


col1, col2 = st.columns(2)
with col1:
    # Input selection
    selected_country = st.selectbox("Select a Country", [
        "Austria", "Belgium", "Bulgaria", "Croatia", "Czechia",
        "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
        "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
        "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
        "Slovenia", "Spain", "Sweden"
    ])  
    st.caption("Note: Complete Cyprus data is not available at the moment.")
with col2:
    selected_year = st.number_input("Select Year", min_value=2015, max_value=2024, step=1, value=2023)

# Fetch data for both sexes
sexes = ["males", "females"]
data = []

for sex in sexes:
    params = {
        "country_name": selected_country,
        "year": str(selected_year),
        "sex": sex
    }
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        results = response.json()
        for row in results:
            emp_all = row["emp_all"]
            data.append({
                "Sex": sex,
                "Average Weekly Hours": emp_all,
                "Age Group": row["age_group"]
            })
    else:
        st.error(f"Failed to fetch data for sex: {sex} (Status Code: {response.status_code})")

# Convert to DataFrame
if data:
    df = pd.DataFrame(data)

    # Average across all age groups for each sex
    avg_df = df.groupby("Sex")["Average Weekly Hours"].mean().reset_index()

    # Plot
    fig = px.bar(
        avg_df,
        x="Sex",
        y="Average Weekly Hours",
        color="Sex",
        title=f"Average Weekly Working Hours by Sex in {selected_country} ({selected_year})",
        labels={"Average Weekly Hours": "Hours"}
    )
else:
    st.warning("No data available for the selected country and year.")


tab1, tab2, tab3 = st.tabs(["Average Weekly Working Hours by Gender ", " Public Spending on Family Benefits ", " Consumer Price Index (CPI) Over Time"])

with tab1:
    st.plotly_chart(fig, use_container_width=True)


with tab2: 
    # Public Expenidtures Table
    benefit_type = []
    expenditures = []
    unit_measured = []
    group = []
    country = []
    year = []

    country_map = {
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

    try: 
        API_URL = "http://web-api:4000/benefits/benefit"
        name_to_code = {v: k for k, v in country_map.items()}

        # Convert selected full country names to country codes
        selected_country_code = name_to_code[selected_country] if selected_country in name_to_code else None
        params = {
            "country_code": selected_country_code,
            "year": selected_year,
            "unit_measured": 'Million Euros',
            'target_group': "All Parents"  
        }

        response1 = requests.get(API_URL, params=params)
        if response1.status_code == 200:
            data = response1.json()

            for item in data:
                benefit_type.append(item['benefit_type'])
                expenditures.append(item['expenditure'])
                unit_measured.append(item['unit_measured'])
                country.append(item['country_code'])
                group.append(item['target_group'])
                country.append(item['country_code'])


    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

    df = pd.DataFrame (
        {
            "Benefit": benefit_type,
            "Expenditure": expenditures,
            "Unit Measured": unit_measured,
        }
    )

    # Display
    st.subheader(f"{selected_country} Benefit Expenditures")
    st.table(df)


with tab3:
    #CPI Viz
    API_URL = "http://web-api:4000/cpi/cpi"  # Adjust host/port if needed
    params = {"country_name": selected_country}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        if data:
            # Convert to DataFrame
            cpi_df = pd.DataFrame(data, columns=["eucpi_id", "country_name", "year", "cpi_value"])

            # Data cleanup
            cpi_df["year"] = cpi_df["year"].astype(int)
            cpi_df["cpi_value"] = pd.to_numeric(cpi_df["cpi_value"], errors="coerce")

            # Sort by year just in case
            cpi_df.sort_values("year", inplace=True)

            # Plot
            fig_cpi = go.Figure()
            fig_cpi.add_trace(go.Scatter(
                x=cpi_df["year"],
                y=cpi_df["cpi_value"],
                mode="lines+markers",
                name="CPI",
                line=dict(color="orange", width=3)
            ))

            fig_cpi.update_layout(
                xaxis_title="Year",
                yaxis_title="CPI",
                height=400,
                title=f"{selected_country} CPI Trend"
            )

            st.plotly_chart(fig_cpi, use_container_width=True)
        else:
            st.info("No CPI data available for this country.")
    else:
        st.error(f"API request failed with status code {response.status_code}")


import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import requests
import pandas as pd
import plotly.express as px
import pycountry

st.set_page_config(page_title="EU Country Predictor", layout="wide")


# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()
AlwaysShowAtBottom()

st.title("Find EU Members by Childcare Spending")

df = pd.read_csv("datasets/parent/3Expenditure.csv")

daycare_df = df[
    (df['benefit_type'] == "Childcare services") &
    (df['unit'] == "Million Euros (2015 prices)")
].copy()

daycare_df['expenditure'] = pd.to_numeric(daycare_df['expenditure'], errors='coerce')
latest_daycare = daycare_df.sort_values("year").groupby("country").tail(1)

# Fix EL → GR for Greece
latest_daycare['country'] = latest_daycare['country'].replace({'EL': 'GR'})

# Country code conversions
def iso2_to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

def iso2_to_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

latest_daycare['iso_alpha'] = latest_daycare['country'].apply(iso2_to_iso3)
latest_daycare['country_name'] = latest_daycare['country'].apply(iso2_to_name)

# Drop invalid
latest_daycare = latest_daycare.dropna(subset=["iso_alpha", "expenditure"])

# Convert to euros
latest_daycare['expenditure_eur'] = latest_daycare['expenditure'] * 1_000_000

# Choropleth plot
fig = px.choropleth(
    latest_daycare,
    locations="iso_alpha",
    locationmode="ISO-3",
    color="expenditure_eur",
    hover_name="country_name",
    hover_data={"expenditure_eur": ":,.0f"},
    color_continuous_scale="YlGnBu",
    title="Childcare Services Expenditures by EU Country (Most Recent Year)",
    template="plotly_white",
    scope="europe"
)

fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False),
    coloraxis_colorbar_title="€ Spent on Childcare (EUR)",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

# create a 2 column layout
col1, col2 = st.columns(2)

# add one number input for variable 1 into column 1
with col1:
    var_01 = st.number_input("Variable 01:", step=1)

# add another number input for variable 2 into column 2
with col2:
    var_02 = st.number_input("Variable 02:", step=1)

logger.info(f"var_01 = {var_01}")
logger.info(f"var_02 = {var_02}")

# add a button to use the values entered into the number field to send to the
# prediction function via the REST API
if st.button("Calculate Prediction", type="primary", use_container_width=True):
    results = requests.get(f"http://web-api:4000/prediction/{var_01}/{var_02}")
    json_results = results.json()
    st.dataframe(json_results)

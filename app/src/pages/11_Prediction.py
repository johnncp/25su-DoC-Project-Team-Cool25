import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Prediction with Regression")

# Page configuration
st.set_page_config(page_title="Birth Rate Predictor", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Paul E. Tishian")  # Placeholder image
    st.markdown("## Navigation")
    st.button("Home")
    st.button("About")
    st.button("Logout")

# Title
st.title("👶 Birth Rate Predictor")

# Input layout
col1, col2, col3 = st.columns([1.2, 1.2, 1])

with col1:
    weekly_hours = st.slider("Weekly Hours", min_value=0, max_value=60, value=30)
    social_protection = st.number_input("Social Protection Benefits (€)", value=0.0, step=10.0)
    child_allowance = st.number_input("Family or Child Allowance (€)", value=0.0, step=10.0)

with col2:
    childcare = st.slider("Child Day Care (€)", min_value=0, max_value=5000, value=1000)
    birth_grant = st.number_input("Birth Grant (€)", value=0.0, step=10.0)
    parental_leave = st.number_input("Parental Leave (weeks)", value=0.0, step=1.0)

with col3:
    country = st.selectbox("Country", ["Belgium", "France", "Germany", "Italy", "Spain", "Sweden"])
    income_maintenance = st.number_input("Income Maintenance (€)", value=0.0, step=10.0)

# Prediction logic (placeholder)
# Replace with ML model or actual function
predicted_birth_rate = 6.0  # dummy placeholder

st.markdown("---")
st.markdown(f"### 🍼 Predicted Birth Rate: **{predicted_birth_rate:.1f}%**")

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

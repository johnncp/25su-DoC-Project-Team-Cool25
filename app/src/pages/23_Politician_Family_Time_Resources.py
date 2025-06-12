import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import requests

st.set_page_config(page_title="Birth Rate Predictor", layout="wide")

SideBarLinks()
AlwaysShowAtBottom()

eu_countries = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden"
]

st.title('Birth Rate Predictor')

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
    country = st.selectbox("Country", eu_countries)
    income_maintenance = st.number_input("Income Maintenance (€)", value=0.0, step=10.0)

# Prediction logic (placeholder)
# Replace with ML model or actual function
predicted_birth_rate = 6.0  # dummy placeholder

st.markdown("---")
st.markdown(f"### 🍼 Predicted Birth Rate: **{predicted_birth_rate:.1f}%**")

st.divider()

"""

st.write('\n\n')
st.write('## Model 1 Maintenance')

st.button("Train Model 01", 
            type = 'primary', 
            use_container_width=True)

st.button('Test Model 01', 
            type = 'primary', 
            use_container_width=True)

if st.button('Model 1 - get predicted value for 10, 25', 
             type = 'primary',
             use_container_width=True):
  results = requests.get('http://web-api:4000/prediction/10/25').json()
  st.dataframe(results)

"""
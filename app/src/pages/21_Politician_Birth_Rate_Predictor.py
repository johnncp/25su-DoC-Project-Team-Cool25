import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(page_title="Birth Rate Predictor", layout="wide")

SideBarLinks()

# ---- Title ----
st.title("Birth Rate Predictor 🍼")
st.markdown("Use the sliders and inputs below to estimate predicted birth rate based on select factors.")

# ---- Input Section ----
st.header("Input Parameters")

col1, col2 = st.columns(2)

with col1:
    weekly_hours = st.slider("Weekly Hours Worked", min_value=0, max_value=60, value=30)

with col2:
    cash = st.number_input("Cash Benefits per Capita (€)", value=0.0, step=100.0)
    services = st.number_input("Childcare Services per Capita (€)", value=0.0, step=50.0)
    maternity = st.number_input("Maternity Spending per Capita (€)", value=0.0, step=50.0)

# Convert inputs to numbers
weekly_hours = int(weekly_hours)
cash = int(cash)
maternity = int(maternity)
services = int(services)

# ---- Prediction Logic ----
try:
    response = requests.get("http://web-api:4000/euro_apis/m1weights")
    response.raise_for_status()
    weights_list = response.json()

    weights = {row["feature_name"]: float(row["weight"]) for row in weights_list}

    prediction = (
        weights.get("intercept", 0)
        + weekly_hours * weights.get("weekly_hours", 0)
        + cash * weights.get("cash_per_capita", 0)
        + maternity * weights.get("maternity_per_capita", 0)
        + services * weights.get("services_per_capita", 0)
    )
    prediction = max(0, prediction)

    st.success(f"🍼 **Predicted Birth Rate:** {prediction:.2f} births per 1000 people")
    st.balloons()

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch model weights: {e}")

# ---- Optional: Expandable for Weights ----
with st.expander("📊 View Model Weights"):
    st.write(pd.DataFrame(weights_list))
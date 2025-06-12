"""import logging
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

    # ---- Optional: Expandable for Weights ----
    with st.expander("📊 View Model Weights"):
        st.write(pd.DataFrame(weights_list))

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch model weights: {e}")
# ---- Optional: Expandable for Weights ----
#with st.expander("📊 View Model Weights"):
    #st.write(pd.DataFrame(weights_list))
"""
import logging
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

# --- Config & Sidebar ---
logger = logging.getLogger(__name__)
st.set_page_config(page_title="Birth Rate Predictor", layout="wide")

st.title("Birth Rate Predictor 🍼")
st.markdown("Select a country and adjust the inputs to estimate its predicted birth rate for 2024.")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Model_data.csv")
    return df.dropna(subset=[
        'birth_rate_per_thousand', 'weekly_hours',
        'cash_per_capita', 'maternity_per_capita',
        'services_per_capita', 'year'
    ])

df = load_data()
all_countries = sorted(df['Country'].dropna().unique())

# --- Country Selection ---
user_country = st.selectbox("Select your country", all_countries)

# --- Fetch most recent data before 2024 ---
def get_latest_country_data(df, country_name):
    country_df = df[(df['Country'] == country_name) & (df['year'] < 2024)]
    if country_df.empty:
        return None
    latest = country_df.sort_values('year', ascending=False).iloc[0]
    return latest

latest_data = get_latest_country_data(df, user_country)

if latest_data is None:
    st.error("No valid data available for this country.")
    st.stop()

# --- Input Sliders ---
st.subheader("Adjust Features for Prediction")

col1, col2 = st.columns(2)

with col1:
    weekly_hours = st.slider("Weekly Hours Worked", 0, 60, int(latest_data['weekly_hours']))
    maternity = st.number_input("Maternity Spending per Capita (€)", value=int(latest_data['maternity_per_capita']), step=50)

with col2:
    cash = st.number_input("Cash Benefits per Capita (€)", value=int(latest_data['cash_per_capita']), step=100)
    services = st.number_input("Childcare Services per Capita (€)", value=int(latest_data['services_per_capita']), step=50)

# --- Load Model Weights from API ---
try:
    response = requests.get("http://web-api:4000/euro_apis/m1weights")  # Your backend endpoint
    response.raise_for_status()
    weights_list = response.json()

    weights = {row["feature_name"]: float(row["weight"]) for row in weights_list}

    # --- Compute squared features ---
    weekly_hours_sq = weekly_hours ** 2
    cash_sq = cash ** 2
    services_sq = services ** 2

    # --- Compute prediction manually ---
    prediction = (
        weights.get("intercept", 0)
        + weekly_hours * weights.get("weekly_hours", 0)
        + maternity * weights.get("maternity_per_capita", 0)
        + services * weights.get("services_per_capita", 0)
        + 2024 * weights.get("year", 0)
        + weekly_hours_sq * weights.get("weekly_hours_squared", 0)
        + cash_sq * weights.get("cash_per_capita_squared", 0)
        + services_sq * weights.get("services_per_capita_squared", 0)
    )

    prediction = max(0, prediction)

    st.success(f"🍼 **Predicted Birth Rate for {user_country} in 2024:** {prediction:.2f} births per 1000 people")
    st.balloons()

    # --- View Model Weights ---
    with st.expander("📊 View Model Weights"):
        st.write(pd.DataFrame(weights_list))

    # --- Visualization of Actual + Predicted ---
    st.subheader(f"📈 Birth Rate Trend for {user_country} with 2024 Prediction")

    country_hist = df[df['Country'] == user_country].copy()
    country_hist = country_hist.sort_values("year")

    if not country_hist.empty:
        last_actual_year = country_hist['year'].max()
        last_actual_value = country_hist[country_hist['year'] == last_actual_year]['birth_rate_per_thousand'].values[0]

        fig = go.Figure()

        # Historical data
        fig.add_trace(go.Scatter(
            x=country_hist['year'],
            y=country_hist['birth_rate_per_thousand'],
            mode='lines+markers',
            name='Actual Birth Rate',
            line=dict(color='blue')
        ))

        # Prediction line
        fig.add_trace(go.Scatter(
            x=[last_actual_year, 2024],
            y=[last_actual_value, prediction],
            mode='lines+markers',
            name='Predicted 2024',
            line=dict(color='orange', dash='dash'),
            marker=dict(color='orange', size=10)
        ))

        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Birth Rate per 1000 People',
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)

except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Failed to fetch model weights: {e}")
import logging
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back

# config & Sidebar
logger = logging.getLogger(__name__)
st.set_page_config(page_title="Birth Rate Predictor", layout="wide")
SideBarLinks()
Back("20_Politician_Home.py")

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
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
        transform: translate(-100%, -80%);
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
    <div class="overlay-text">Birth Rate Predictor 🍼</div>
""", unsafe_allow_html=True)

# data
@st.cache_data
def load_data():
    df = pd.read_csv("datasets/model1/Model_data.csv")
    df = df.dropna(subset=[
        'birth_rate_per_thousand', 'weekly_hours',
        'cash_per_capita', 'maternity_per_capita',
        'services_per_capita', 'year'
    ])
    # remove EU
    excluded = ["EU28", "EU Average", "Euro area", "EU27_2020", "EA19"]
    return df[~df["Country"].isin(excluded)]

df = load_data()
all_countries = sorted(df["Country"].dropna().unique())

st.markdown("Select a country and adjust the inputs to estimate its predicted birth rate for 2024.")
st.info("← Customize your criteria on the sidebar.")

st.markdown("### Wondering what these features mean?")
            
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **💼 Work-Life Balance (Weekly Hours)**: Average working hours per week. Lower is generally better for work-life balance.
                
    **💰 Cash Support**: Government cash benefits per capita (€). Higher means more financial support.
     """)
            
with col2:
    st.markdown("""
    **👶 Maternity Support**: Maternity benefits per capita (€). Higher means better parental support.
                
    **🏥 Public Services**: Public services spending per capita (€). Higher means better public services.
    """)
st.markdown("""
The values you see loaded in already come from that countries 2023 data, adjust to see the changes!"""
)           
st.divider()
            
# country selection 
user_country = st.sidebar.selectbox("Select your country", all_countries)

# fetch most recent data before 2024
def get_latest_country_data(df, country_name):
    country_df = df[(df['Country'] == country_name) & (df['year'] < 2024)]
    if country_df.empty:
        return None
    return country_df.sort_values('year', ascending=False).iloc[0]

latest_data = get_latest_country_data(df, user_country)
if latest_data is None:
    st.error("No valid data available for this country.")
    st.stop()

# input sliders 
st.subheader("Adjust Features for Prediction")

col1, col2 = st.columns(2)

with col1:
    weekly_hours = st.sidebar.slider("Weekly Hours Worked", 0, 60, 30)

with col2:
    cash = st.sidebar.number_input("Cash Benefits per Capita (€)", 40000, step=100)
    services = st.sidebar.number_input("Childcare Services per Capita (€)", 20000, step=50)
    maternity = st.sidebar.number_input("Maternity Spending per Capita (€)", 300, step=50)

# load Model Weights + predict
try:
    response = requests.get("http://web-api:4000/euro_apis/m1weights") 
    response.raise_for_status()
    weights_list = response.json()
    weights = {row["feature_name"]: float(row["weight"]) for row in weights_list}

    # Means and stds from training data
    mean_vals = {
        'weekly_hours': 37.88517,
        'maternity_per_capita': 247.1181,
        'services_per_capita': 26039.31,
        'year': 2018.45,
        'weekly_hours_squared': 1440.816,
        'cash_per_capita_squared': 8.248512e9,
        'services_per_capita_squared': 3.750855e9
    }

    std_vals = {
        'weekly_hours': 2.35736,
        'maternity_per_capita': 656.3605,
        'services_per_capita': 55566.02,
        'year': 2.265675,
        'weekly_hours_squared': 171.7396,
        'cash_per_capita_squared': 2.972042e10,
        'services_per_capita_squared': 1.440493e10
    }

    # Compute and standardize inputs
    weekly_hours_sq = weekly_hours ** 2
    cash_sq = cash ** 2
    services_sq = services ** 2

    features_std = {
        "weekly_hours": (weekly_hours - mean_vals['weekly_hours']) / std_vals['weekly_hours'],
        "maternity_per_capita": (maternity - mean_vals['maternity_per_capita']) / std_vals['maternity_per_capita'],
        "services_per_capita": (services - mean_vals['services_per_capita']) / std_vals['services_per_capita'],
        "year": (2024 - mean_vals['year']) / std_vals['year'],
        "weekly_hours_squared": (weekly_hours_sq - mean_vals['weekly_hours_squared']) / std_vals['weekly_hours_squared'],
        "cash_per_capita_squared": (cash_sq - mean_vals['cash_per_capita_squared']) / std_vals['cash_per_capita_squared'],
        "services_per_capita_squared": (services_sq - mean_vals['services_per_capita_squared']) / std_vals['services_per_capita_squared'],
    }

    # Predict birth rate
    prediction = (
        weights.get("intercept", 0)
        + features_std["weekly_hours"] * weights.get("weekly_hours", 0)
        + features_std["maternity_per_capita"] * weights.get("maternity_per_capita", 0)
        + features_std["services_per_capita"] * weights.get("services_per_capita", 0)
        + features_std["year"] * weights.get("year", 0)
        + features_std["weekly_hours_squared"] * weights.get("weekly_hours_squared", 0)
        + features_std["cash_per_capita_squared"] * weights.get("cash_per_capita_squared", 0)
        + features_std["services_per_capita_squared"] * weights.get("services_per_capita_squared", 0)
    )
    prediction = max(0, prediction)
    st.text(f"Predicted Birth Rate for {user_country} in 2024:")
    st.markdown(
    
        f"""
        <div style='
            padding: 1em; 
            background: linear-gradient(135deg, #0e47cb, #5f99f7); 
            border-radius: 15px;
        '>
            <p style='font-size: 2.2em; font-weight: bold; color: #ffffff; margin: 0;'>
                {prediction:.2f} births per 1000 people
            </p>
        </div>
        """,

        unsafe_allow_html=True

    )
    #st.success(f" **Predicted Birth Rate for {user_country} in 2024:** {prediction:.2f} births per 1000 people")
    #st.balloons()

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch model weights: {e}")
    st.stop()

st.divider()

# --- Visualization of Actual + Predicted ---
st.subheader(f"Birth Rate Trend for {user_country} with 2024 Prediction")

country_hist = df[df['Country'] == user_country].copy().sort_values("year")
if not country_hist.empty:
    last_actual_year = country_hist['year'].max()
    last_actual_value = country_hist[country_hist['year'] == last_actual_year]['birth_rate_per_thousand'].values[0]

    fig = go.Figure()

    # historical line
    fig.add_trace(go.Scatter(
        x=country_hist['year'],
        y=country_hist['birth_rate_per_thousand'],
        mode='lines+markers',
        name='Actual Birth Rate',
        line=dict(color='blue')
    ))

    # prediction line
    fig.add_trace(go.Scatter(
        x=[last_actual_year, 2024],
        y=[last_actual_value, prediction],
        mode='lines+markers',
        name='Predicted 2024',
        line=dict(color='orange', dash='dash'),
        marker=dict(color='orange', size=10)
    ))

    fig.update_traces(
        line_shape='spline',
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Birth Rate per 1000 People',
        template='plotly_white',
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

st.sidebar.divider()
AlwaysShowAtBottom()
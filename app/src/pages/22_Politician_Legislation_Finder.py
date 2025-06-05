import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(page_title="Birth Rate Predictor", layout="wide")

SideBarLinks()

# Visualization Imports
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.title("Legislation Finder")
st.write('\n\n')
st.write('\n\n')
st.write('\n\n')

# --- COUNTRY MAPPING ---
country_map = {
    'EU27_2020': 'European Union (27)',
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

# --- DATA LOAD ---
df = pd.read_csv("datasets/politician/formatted_birth_data.csv")
df["country_name"] = df["country"].map(country_map)
df = df[df["birth_rate_per_thousand"].notna()]

# --- COUNTRY LISTS ---
all_countries = sorted(df["country_name"].dropna().unique())
eu_country = "European Union (27)"

# Separate EU-wide and national countries
national_countries = [c for c in all_countries if c != eu_country]

# Toggles
col1, col2, col3, col4 = st.columns(4)

with col1:
    select_all = st.checkbox("Select all members", value=True)

with col2:
    fixed_range = st.checkbox("Fix the Y-axis", value=True)

# Pre-select logic
pre_selected = national_countries if select_all else [eu_country]

# --- MULTISELECT ---
selected_countries = st.multiselect("Select countries to display:", all_countries, default=pre_selected)

# --- FILTER DATA ---
if selected_countries:
    filtered_df = df[df["country_name"].isin(selected_countries)]
else:
    st.warning("Please select at least one country.")
    st.stop()

# --- PLOT ---
line_width = 2 if len(selected_countries) <= 10 else 1

custom_colors = px.colors.qualitative.Plotly + px.colors.qualitative.Dark24 + px.colors.qualitative.Safe # Colors
country_list = sorted(df["country_name"].unique())
color_map = {country: custom_colors[i % len(custom_colors)] for i, country in enumerate(country_list)}

fig = px.line(
    filtered_df,
    x="year",
    y="birth_rate_per_thousand",
    color="country_name",
    title="Crude Birth Rate Over Time (per 1000 people)",
    labels={
        "year": "Year",
        "birth_rate_per_thousand": "Birth Rate (‰)",
        "country_name": "Country"
    },
    color_discrete_map=color_map,
    line_shape="spline"
)

opacity_value = 0.4

if not select_all:
    opacity_value = 1
else:
    opacity_value = 0.4

fig.update_traces(line=dict(width=3),
                  opacity=opacity_value,
                  mode="lines+markers")

y_axis_config = dict(showgrid=True, gridcolor="lightgrey")
if fixed_range:
    y_axis_config["range"] = [5.5, 14.5]

fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        title_text=None
    ),
    plot_bgcolor="#ffffff",  # White background
    paper_bgcolor="#ffffff",
    xaxis=dict(
        showgrid=True,
        gridcolor="lightgrey",
        zeroline=False
    ),
    yaxis=y_axis_config,
    height=600 if len(selected_countries) <= 10 else 800,
)

# --- DISPLAY ---
st.plotly_chart(fig, use_container_width=True)
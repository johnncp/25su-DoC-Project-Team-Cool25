import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# PAGE SETUP 
st.set_page_config(page_title="Legislation Finder", layout="wide")
SideBarLinks()


st.title("Legislation Finder")
col1, col2 = st.columns(2)
with col1:
    st.text("Discover trends and filter through laws that impact families and child care across the EU.")
st.write('\n\n\n')

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

# DATA LOAD 
df = pd.read_csv("datasets/politician/birth_with_2024.csv")
df["country_name"] = df["country"].map(country_map)
df = df[df["birth_rate_per_thousand"].notna()]

# COUNTRY LISTS 
all_countries = sorted(df["country_name"].dropna().unique())
eu_country = "European Union (27)"
national_countries = [c for c in all_countries if c != eu_country]

# TOGGLES 
with st.sidebar:
    st.subheader("Chart Filters 📈")
    select_all = st.checkbox("Select all members", value=True)
    fixed_range = st.checkbox("Fixed Y-axis", value=True)
    show_predictions = st.checkbox("Show 2024 Predictions", value=True)

st.info("← Customize the chart using the sidebar.")

# MULTISELECT 
pre_selected = national_countries if select_all else [eu_country]
selected_countries = st.multiselect("Select countries to display:", all_countries, default=pre_selected)

# FILTER 
if not selected_countries:
    st.warning("Please select at least one country.")
    st.stop()

filtered_df = df[df["country_name"].isin(selected_countries)]
historical_df = filtered_df[filtered_df["year"] < 2024]
prediction_df = filtered_df[filtered_df["year"] == 2024]

# COLOR 
custom_colors = px.colors.qualitative.Plotly + px.colors.qualitative.Dark24 + px.colors.qualitative.Safe
color_map = {country: custom_colors[i % len(custom_colors)] for i, country in enumerate(all_countries)}


# PLOT 
fig = go.Figure()

for country in selected_countries:
    hist = historical_df[historical_df["country_name"] == country]
    pred = prediction_df[prediction_df["country_name"] == country]

    # Combine historical and prediction if toggle is on
    combined = pd.concat([hist, pred]) if show_predictions else hist

    # Plot continuous line
    fig.add_trace(go.Scatter(
        x=combined["year"],
        y=combined["birth_rate_per_thousand"],
        mode="lines+markers",
        name=country,
        line=dict(width=3, color=color_map[country]),
        marker=dict(symbol="circle", size=7),
        legendgroup=country
    ))

    # Emphasize 2024 prediction with diamond marker
    if show_predictions and not pred.empty:
        fig.add_trace(go.Scatter(
            x=pred["year"],
            y=pred["birth_rate_per_thousand"],
            mode="markers",
            name=f"{country} (2024)",
            marker=dict(symbol="diamond", size=11, color=color_map[country]),
            legendgroup=country,
            showlegend=False
        ))

# FINAL STYLING 
fig.update_traces(
    line_shape='spline',
)

fig.update_layout(
    title="Crude Birth Rate Over Time (per 1000 people)",
    xaxis_title="Year",
    yaxis_title="Birth Rate (‰)",
    template="plotly_white",
    height=600 if len(selected_countries) <= 10 else 800,
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    
    xaxis=dict(showgrid=True, gridcolor="lightgrey", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="lightgrey", range=[5.5, 14.5] if fixed_range else None)
)


st.plotly_chart(fig, use_container_width=True)

st.divider()

st.info("← Filter legislations using the sidebar.")

# POLICY API SECTION 
API_URL = "http://web-api:4000/policy/allpolicy"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        policy = response.json()
        
        name_to_code = {v: k for k, v in country_map.items()}
        selected_country_codes = [name_to_code[c] for c in selected_countries if c in name_to_code]

        params = {}
        if selected_country_codes:
            params["country_code"] = ",".join(selected_country_codes)

        focus_areas = sorted(list(set(pol["focus_area"] for pol in policy)))
        founding_years = sorted(list(set(pol["year"] for pol in policy)))

        #selected_focus = st.selectbox("Filter by Focus Area", ["All"] + focus_areas)
        #selected_year = st.selectbox("Filter by Year", ["All"] + [str(year) for year in founding_years])

        with st.sidebar:
            st.divider()
            st.subheader("Legislation Filters 📑")
            selected_focus = st.selectbox("Filter by Focus Area", ["All"] + focus_areas)
            selected_year = st.selectbox("Filter by Year", ["All"] + [str(year) for year in founding_years])
                
        

        if selected_focus != "All":
            params["focus_area"] = selected_focus
        if selected_year != "All":
            params["year"] = selected_year

        filtered_response = requests.get(API_URL, params=params)
        if filtered_response.status_code == 200:
            filtered_policy = filtered_response.json()
            st.write(f"Found {len(filtered_policy)} Policies")

            cols = st.columns(3)

            for idx, pol in enumerate(filtered_policy):
                with cols[idx % 3].expander(f"{pol['policy_name']} ({pol['country_code']})"):
                    st.write("**Basic Information**")
                    st.write(f"**Country:** {pol['country_code']}")
                    st.write(f"**Year Passed:** {pol['year']}")
                    st.write(f"**Focus Area:** {pol['focus_area']}")
                    st.write("**Description:**")
                    st.write(pol['description'])

    else:
        st.error("Failed to fetch Policy data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")

st.sidebar.divider()
AlwaysShowAtBottom()
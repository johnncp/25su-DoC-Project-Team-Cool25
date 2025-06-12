"""
import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests



st.set_page_config(page_title="Legislation Finder", layout="wide")

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
    fixed_range = st.checkbox("Fixed Y-axis", value=True)

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


# API endpoint
API_URL = "http://web-api:4000/policy/allpolicy"

# Create filter columns
col1, col2, col3 = st.columns(3)

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        policy = response.json()

        # Extract unique values for filters
        # Invert country_map: full country name -> code
        name_to_code = {v: k for k, v in country_map.items()}

        # Convert selected full country names to country codes
        selected_country_codes = [name_to_code[c] for c in selected_countries if c in name_to_code]

        params = {}
        #params = []
        # Filter policies by selected country codes
        if selected_country_codes:
            #filtered_policy = [pol for pol in policy if pol['country_code'] in selected_country_codes]
            #params["country_code"] = selected_country_codes
            #params["country_code"] = ",".join(selected_country_codes)
            params["country_code"] = ",".join(selected_country_codes)

        #for code in selected_country_codes:
            #params.append(('country_code', code))

        #else:
            #filtered_policy = policy  # no filtering if none selected
        #countries = sorted(list(set(pol["country_code"] for pol in policy)))
        focus_areas = sorted(list(set(pol["focus_area"] for pol in policy)))
        founding_years = sorted(list(set(pol["year"] for pol in policy)))

        # Create filters
        with col1:
            #selected_country = st.selectbox("Filter by Country", ["All"] + countries)

        #with col2:
            selected_focus = st.selectbox("Filter by Focus Area", ["All"] + focus_areas)

        with col2:
            selected_year = st.selectbox(
                "Filter by Year",
                ["All"] + [str(year) for year in founding_years],
            )

        # Build query parameters

        #if selected_country != "All":
            #params["country_code"] = selected_country
        if selected_focus != "All":
            params["focus_area"] = selected_focus
            #params.append(('focus_area', selected_focus))

        if selected_year != "All":
            params["year"] = selected_year
            #params.append(('year', selected_year))


        #if selected_focus != "All":
            #filtered_policy = [pol for pol in filtered_policy if pol["focus_area"] == selected_focus]
       #if selected_year != "All":
            #filtered_policy = [pol for pol in filtered_policy if str(pol["year"]) == selected_year]

        # Get filtered data
        filtered_response = requests.get(API_URL, params=params)
        if filtered_response.status_code == 200:
            filtered_policy = filtered_response.json()

            # Display results count
            st.write(f"Found {len(filtered_policy)} Policies")

            # Create expandable rows for each NGO
            for pol in filtered_policy:
                with st.expander(f"{pol['policy_name']} ({pol['country_code']})"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Basic Information**")
                        st.write(f"**Country:** {pol['country_code']}")
                        st.write(f"**Year Passed:** {pol['year']}")
                        st.write(f"**Focus Area:** {pol['focus_area']}")

                    with col2:
                        st.write("\n\n")
                        st.write(f"**Description:** {pol['description']})")

                    

    else:
        st.error("Failed to fetch Policy data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
"""
import logging
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from modules.nav import SideBarLinks

# CONFIG
logger = logging.getLogger(__name__)
st.set_page_config(page_title="Legislation Finder", layout="wide")
SideBarLinks()
st.title("Legislation Finder")

# MAPPING
country_map = {
    'EU27_2020': 'European Union (27)', 'BE': 'Belgium', 'BG': 'Bulgaria',
    'CZ': 'Czechia', 'DK': 'Denmark', 'DE': 'Germany', 'EE': 'Estonia',
    'IE': 'Ireland', 'EL': 'Greece', 'ES': 'Spain', 'FR': 'France', 'HR': 'Croatia',
    'IT': 'Italy', 'CY': 'Cyprus', 'LV': 'Latvia', 'LT': 'Lithuania',
    'LU': 'Luxembourg', 'HU': 'Hungary', 'MT': 'Malta', 'NL': 'Netherlands',
    'AT': 'Austria', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania',
    'SI': 'Slovenia', 'SK': 'Slovakia', 'FI': 'Finland', 'SE': 'Sweden'
}

# LOAD DATA
df = pd.read_csv("datasets/model1/Model_data.csv")
df["country"] = df["Country"]
df["country_name"] = df["country"].map(country_map)
df = df[df["birth_rate_per_thousand"].notna()]

# MODEL WEIGHTS AND COMPUTE 2024 PREDS
try:
    response = requests.get("http://web-api:4000/euro_apis/m1weights")
    response.raise_for_status()
    weights_list = response.json()
    weights = {row["feature_name"]: float(row["weight"]) for row in weights_list}

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

    preds = []
    for country in df['country'].unique():
        latest = df[(df['country'] == country) & (df['year'] < 2024)].sort_values('year', ascending=False).head(1)
        if latest.empty:
            continue

        row = latest.iloc[0]
        weekly_hours = row['weekly_hours']
        cash = row['cash_per_capita']
        maternity = row['maternity_per_capita']
        services = row['services_per_capita']

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

        preds.append({
            "country": country,
            "year": 2024,
            "birth_rate_per_thousand": max(0, prediction),
            "country_name": country_map.get(country, country)
        })

    df_preds = pd.DataFrame(preds)
    df = pd.concat([df, df_preds], ignore_index=True)

except requests.exceptions.RequestException as e:
    st.warning("Could not fetch model weights. 2024 predictions skipped.")
    logger.error(e)

# UI
all_countries = sorted(df["country_name"].dropna().unique())
eu_country = "European Union (27)"
national_countries = [c for c in all_countries if c != eu_country]

col1, col2, col3 = st.columns(3)
with col1:
    select_all = st.checkbox("Select all members", value=True)
with col2:
    fixed_range = st.checkbox("Fixed Y-axis", value=True)
with col3:
    show_pred = st.checkbox("Include 2024 Predictions", value=True)

pre_selected = national_countries if select_all else [eu_country]
selected_countries = st.multiselect("Select countries to display:", all_countries, default=pre_selected)

if not selected_countries:
    st.warning("Please select at least one country.")
    st.stop()

filtered_df = df[df["country_name"].isin(selected_countries)]

# COLOR MAP
import plotly.express as px
custom_colors = px.colors.qualitative.Plotly + px.colors.qualitative.Dark24 + px.colors.qualitative.Safe
color_map = {country: custom_colors[i % len(custom_colors)] for i, country in enumerate(all_countries)}

# PLOT
fig = go.Figure()

for country in selected_countries:
    country_data = filtered_df[filtered_df["country_name"] == country].sort_values("year")
    hist = country_data[country_data["year"] < 2024]
    pred = country_data[country_data["year"] == 2024]

    # Historical line
    fig.add_trace(go.Scatter(
        x=hist["year"],
        y=hist["birth_rate_per_thousand"],
        mode="lines+markers",
        name=f"{country} (Actual)",
        line=dict(color=color_map.get(country, "gray"), width=3),
        marker=dict(size=6)
    ))

    # 2024 prediction line (even if no history)
    if show_pred and not pred.empty:
        if not hist.empty:
            last_actual_year = hist["year"].iloc[-1]
            last_actual_value = hist["birth_rate_per_thousand"].iloc[-1]
        else:
            last_actual_year = 2023
            last_actual_value = 0

        fig.add_trace(go.Scatter(
            x=[last_actual_year, 2024],
            y=[last_actual_value, pred["birth_rate_per_thousand"].iloc[0]],
            mode="lines+markers",
            name=f"{country} (Predicted 2024)",
            line=dict(color="orange", dash="dash", width=3),
            marker=dict(color="orange", size=8, symbol="diamond")
        ))

# FINAL LAYOUT 
fig.update_layout(
    title="Crude Birth Rate Over Time (with Optional 2024 Prediction)",
    xaxis_title="Year",
    yaxis_title="Birth Rate (‰)",
    template="plotly_white",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    height=600 if len(selected_countries) <= 10 else 800
)

fig.update_xaxes(showgrid=True, gridcolor="lightgrey", zeroline=False)
fig.update_yaxes(showgrid=True, gridcolor="lightgrey")
if fixed_range:
    fig.update_yaxes(range=[5.5, 14.5])

st.plotly_chart(fig, use_container_width=True)

# API endpoint
API_URL = "http://web-api:4000/policy/allpolicy"

# Create filter columns
col1, col2, col3 = st.columns(3)

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        policy = response.json()

        # Extract unique values for filters
        # Invert country_map: full country name -> code
        name_to_code = {v: k for k, v in country_map.items()}

        # Convert selected full country names to country codes
        selected_country_codes = [name_to_code[c] for c in selected_countries if c in name_to_code]

        params = {}
        #params = []
        # Filter policies by selected country codes
        if selected_country_codes:
            #filtered_policy = [pol for pol in policy if pol['country_code'] in selected_country_codes]
            #params["country_code"] = selected_country_codes
            #params["country_code"] = ",".join(selected_country_codes)
            params["country_code"] = ",".join(selected_country_codes)

        #for code in selected_country_codes:
            #params.append(('country_code', code))

        #else:
            #filtered_policy = policy  # no filtering if none selected
        #countries = sorted(list(set(pol["country_code"] for pol in policy)))
        focus_areas = sorted(list(set(pol["focus_area"] for pol in policy)))
        founding_years = sorted(list(set(pol["year"] for pol in policy)))

        # Create filters
        with col1:
            #selected_country = st.selectbox("Filter by Country", ["All"] + countries)

        #with col2:
            selected_focus = st.selectbox("Filter by Focus Area", ["All"] + focus_areas)

        with col2:
            selected_year = st.selectbox(
                "Filter by Year",
                ["All"] + [str(year) for year in founding_years],
            )

        # Build query parameters

        #if selected_country != "All":
            #params["country_code"] = selected_country
        if selected_focus != "All":
            params["focus_area"] = selected_focus
            #params.append(('focus_area', selected_focus))

        if selected_year != "All":
            params["year"] = selected_year
            #params.append(('year', selected_year))


        #if selected_focus != "All":
            #filtered_policy = [pol for pol in filtered_policy if pol["focus_area"] == selected_focus]
       #if selected_year != "All":
            #filtered_policy = [pol for pol in filtered_policy if str(pol["year"]) == selected_year]

        # Get filtered data
        filtered_response = requests.get(API_URL, params=params)
        if filtered_response.status_code == 200:
            filtered_policy = filtered_response.json()

            # Display results count
            st.write(f"Found {len(filtered_policy)} Policies")

            # Create expandable rows for each NGO
            for pol in filtered_policy:
                with st.expander(f"{pol['policy_name']} ({pol['country_code']})"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Basic Information**")
                        st.write(f"**Country:** {pol['country_code']}")
                        st.write(f"**Year Passed:** {pol['year']}")
                        st.write(f"**Focus Area:** {pol['focus_area']}")

                    with col2:
                        st.write("\n\n")
                        st.write(f"**Description:** {pol['description']})")

                    

    else:
        st.error("Failed to fetch Policy data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
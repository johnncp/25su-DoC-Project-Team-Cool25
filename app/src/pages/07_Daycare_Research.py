import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pycountry
import os


Back("04_Business_Planner.py")
SideBarLinks()
AlwaysShowAtBottom()

st.markdown("""
## Thinking of expanding your daycare business?

This page gives you a snapshot of how daycare centers are performing across different countries. 
            Curious about how many children are typically enrolled? Or how large the average staff is in each center? 
            Use this tool to compare trends, spot opportunities, and get a feel for what operating a daycare might look like in the country you're considering.
""")
st.markdown("#### Things to Consider When Expanding:")
st.markdown("""
- Are enrollment numbers growing year over year?
- Does CPI suggest operating costs are manageable?
- Are staffing levels consistent across different centers?
- Is this market oversaturated or still growing?
""")

# 1. Get all locations (only active ones returned by your route)
locations_response = requests.get("http://web-api:4000/location/locations")
locations_data = locations_response.json()
df_locations = pd.DataFrame(locations_data)

# 2. Get all daycare data (raw data, all rows)
data_response = requests.get("http://web-api:4000/daycaredata/data")
data_data = data_response.json()
df_data = pd.DataFrame(data_data)

# 3. Merge & preprocess
df = pd.merge(df_data, df_locations, on="daycare_id")
df = df[df["inactive"] == False]  # Filter to active only

# Ensure correct types
df["year"] = df["Year"].astype(int)
df["daycare_display_name"] = df["daycare_name"] + " (" + df["city"] + ")"

# 4. Country map
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
df["country_full"] = df["country_code"].map(country_map)



# 5. Dropdown to select country
available_countries = sorted(df["country_full"].dropna().unique())
selected_country = st.selectbox("Select Country", available_countries)
selected_country_code = df[df["country_full"] == selected_country]["country_code"].iloc[0]


# 6. Filter by country and group by year
filtered_df = df[df["country_full"] == selected_country]
summary = filtered_df.groupby("year")["Enrollment"].mean().reset_index()

# 7. Plot
fig = px.bar(
    summary,
    x="year",
    y="Enrollment",
    title=f"Average Daycare Enrollment in {selected_country} Over Time"
)
fig.update_layout(xaxis_title="Year", yaxis_title="Average Enrollment")
fig.show()

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    for _ in range(14):
        st.write("\n\n")
    st.markdown(f"See how daycare enrollment has changed in **{selected_country}** year by year. This can help you spot growth trends and estimate demand.")

# --- BAR CHART: Enrollment + Staff by daycare for latest year ---

# --- Filter to latest year ---
latest_year = df["year"].max()
bar_df = df[(df["year"] == latest_year) & (df["country_code"] == selected_country_code)].copy()
bar_df.sort_values(by="Enrollment", ascending=False, inplace=True)

# --- Plot ---
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=bar_df["daycare_display_name"],
    y=bar_df["Enrollment"],
    name="Enrollment",
    marker_color="steelblue"
))
fig_bar.add_trace(go.Bar(
    x=bar_df["daycare_display_name"],
    y=bar_df["Staff"],
    name="Staff",
    marker_color="indianred"
))

fig_bar.update_layout(
    title=f"Enrollment vs. Staff in {selected_country} ({latest_year})",
    barmode="group",
    xaxis=dict(
        title="Daycare (with city)",
        tickangle=45,
        tickfont=dict(size=11),
        title_font=dict(size=14),
    ),
    yaxis=dict(
        title="Count",
        title_font=dict(size=14),
        tickformat=",",
        tickfont=dict(size=12),
    ),
    height=600
)


with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
with col2: 
    for _ in range(24):
        st.write("\n\n")
    st.markdown(f"In **{selected_country}**, here’s how different daycare locations compare in terms of how many children they serve and how many staff they employ.")

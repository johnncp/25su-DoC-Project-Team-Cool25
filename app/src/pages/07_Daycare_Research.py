import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pycountry
import os

SideBarLinks()
AlwaysShowAtBottom()

# datasets
df_data = pd.read_csv("datasets/parent/DaycareData.csv")
df_locations = pd.read_csv("datasets/parent/DaycareLocations.csv", encoding="ISO-8859-1")


# Merge and filter
df = pd.merge(df_data, df_locations, on="daycare_id")
df = df[df["inactive"] == False]  # active only
df["year"] = df["year"].astype(int)
df["daycare_display_name"] = df["daycare_name"] + " (" + df["city"] + ")"

# Get sorted country list
available_countries = sorted(df["country_code"].unique())
selected_country = st.selectbox("Select a country:", available_countries)

# --- LINE CHART: Avg enrollment over time ---
trend_df = df[df["country_code"] == selected_country].groupby("year")["enrollment"].mean().reset_index()

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=trend_df["year"],
    y=trend_df["enrollment"],
    mode='lines+markers',
    name=selected_country
))

fig_line.update_layout(
    title=f"Avg Enrollment Over Time – {selected_country}",
    xaxis_title="Year",
    yaxis_title="Average Enrollment",
    height=500
)

st.plotly_chart(fig_line, use_container_width=True)

# --- BAR CHART: Enrollment + Staff by daycare for latest year ---
latest_year = df["year"].max()
bar_df = df[(df["year"] == latest_year) & (df["country_code"] == selected_country)].copy()
bar_df.sort_values(by="enrollment", ascending=False, inplace=True)

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=bar_df["daycare_display_name"],
    y=bar_df["enrollment"],
    name="Enrollment",
    marker_color="steelblue"
))
fig_bar.add_trace(go.Bar(
    x=bar_df["daycare_display_name"],
    y=bar_df["staff"],
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

st.plotly_chart(fig_bar, use_container_width=True)
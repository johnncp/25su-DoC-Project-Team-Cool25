import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import requests

SideBarLinks()
AlwaysShowAtBottom()

st.title('Resources')


# Load and filter data
df = pd.read_csv("datasets/parent/workhour_total.csv")
df_2024 = df[
    (df['TIME_PERIOD'] == 2024) &
    (df['sex'].isin(['Males', 'Females'])) &
    (df['OBS_VALUE'].notna())
].copy()

df_2024['sex'] = df_2024['sex'].replace({'Males': 'Male', 'Females': 'Female'})
df_2024 = df_2024[['geo', 'sex', 'OBS_VALUE']]
df_2024.columns = ['country', 'sex', 'average_hours']

# Reshape and keep only countries with both Male and Female data
pivot = df_2024.pivot(index='country', columns='sex', values='average_hours').dropna().reset_index()
df_clean = pivot.melt(id_vars='country', value_vars=['Male', 'Female'],
                      var_name='sex', value_name='average_hours')

# List of EU countries with EU27_2020 at the end
eu_countries = df_clean[df_clean['country'] != 'EU27_2020']['country'].unique().tolist()
eu_countries.sort()
eu_countries.append('EU27_2020')

# Streamlit selectbox for country selection
selected_country = st.selectbox("Select a country", eu_countries)

# Filter data for selected country
selected_data = df_clean[df_clean['country'] == selected_country]

# Colors
colors = {'Male': 'blue', 'Female': 'pink'}

# Build plot
fig = go.Figure()
fig.add_trace(go.Bar(
    x=selected_data['sex'],
    y=selected_data['average_hours'],
    marker_color=[colors[sex] for sex in selected_data['sex']]
))

fig.update_layout(
    title=f'Average Weekly Working Hours in {selected_country} (2024)',
    xaxis_title='Sex',
    yaxis_title='Average Weekly Hours',
    yaxis=dict(tickformat=".1f", dtick=5, range = [0,50]),
    height=600  # Adjust chart size here
)

# Display
st.plotly_chart(fig, use_container_width=True)


benefit_type = []
expenditures = []
unit_measured = []
group = []
country = []

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

try: 
    API_URL = "http://web-api:4000/benefits/benefit"
    name_to_code = {v: k for k, v in country_map.items()}

        # Convert selected full country names to country codes
    selected_country_code = name_to_code[selected_country] if selected_country in name_to_code else None
    params = {
        "country_code": selected_country_code,
        "year": 2022,
        "unit_measured": 'Million Euros',
        'target_group': "All Parents"  
    }

    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()

        for item in data:
            benefit_type.append(item['benefit_type'])
            expenditures.append(item['expenditure'])
            unit_measured.append(item['unit_measured'])
            country.append(item['country_code'])


except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")

df = pd.DataFrame (
    {
        "Benefit": benefit_type,
        "Expenditure": expenditures,
        "Unit Measured": unit_measured,
        "Country": country
    }
)

st.subheader(f"{selected_country} Benefit Expenditures")
st.table(df)
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
from modules.nav import SideBarLinks, AlwaysShowAtBottom, Back
import time
import base64, logging

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(layout="wide")

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Configuration
API_BASE_URL = "http://web-api:4000/model2"  # Adjust based on your Flask server URL

Back("10_Parent_Home.py")

# Helper functions
def get_feature_stats() -> Dict: # return Dict
    """Fetch feature statistics from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/features/stats")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch feature statistics: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None

def get_recommendations(preferences: Dict) -> Dict: # returh Dict
    """Get country recommendations from the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/recommend",
            json=preferences
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get recommendations: {response.status_code}")
            if response.text:
                st.error(response.text)
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None


def create_radar_chart(country_data: Dict, user_prefs: Dict) -> go.Figure: # return go Figure
    """Create a radar chart comparing country features with user preferences"""
    categories = ['Weekly Hours', 'Cash Support', 'Maternity Support', 'Services']
    
    # Normalize country values to 0 to 10 scale
    country_values = [
        10 - (country_data.get('weekly_hours', 40.60) - 30.95) / (40.60 - 30.95) * 10,  # Inverted, Max 40.60, Min 30.95
        country_data.get('cash_per_capita', 0) / 407371 * 10,  # Max 407371
        country_data.get('maternity_per_capita', 0) / 3012.24 * 10,  # Max 3012.24
        country_data.get('services_per_capita', 0) / 309752 * 10  # Max 309752
    ]
    
    user_values = [
        user_prefs['weekly_hours'],
        user_prefs['cash_per_capita'],
        user_prefs['maternity_per_capita'],
        user_prefs['services_per_capita']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=country_values,
        theta=categories,
        fill='toself',
        name='Country',
        line_color='blue'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=user_values,
        theta=categories,
        fill='toself',
        name='Your Preferences',
        line_color='red'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        height=500
    )
    
    return fig

# putting it all together in main

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def fetch_users_by_role(role_id):
    try:
        response = requests.get(f"http://web-api:4000/users/role/{role_id}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching users: {e}")

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
    <div class="overlay-text">🇪🇺 EU Country Recommender</div>
""", unsafe_allow_html=True)

st.markdown("Find the EU countries that best matches your preferences for work-life balance and family support!")

# Sidebar for user preferences
with st.sidebar:
    st.header("Choose Your Preferences ✓ ")
    st.markdown("Rate from **0** (not important) to **10** (very important) for your parenthood priorities.")
    
    preferences = {}
    
    # Weekly Hours slider
    st.subheader("Work-Life Balance ⚖️")
    preferences['weekly_hours'] = st.slider(
        "Preference for shorter working hours",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = preference for countries with shorter working weeks"
    )
    
    # Cash Support slider
    st.subheader("Cash Support 💶")
    preferences['cash_per_capita'] = st.slider(
        "Importance of cash benefits per capita",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = preference for countries with more cash support"
    )
    
    # Maternity Support slider
    st.subheader("Maternity Support 👶")
    preferences['maternity_per_capita'] = st.slider(
        "Importance of maternity benefits",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = preference for countries with better maternity support"
    )
    
    # Services Support slider
    st.subheader("Public Services 🚑")
    preferences['services_per_capita'] = st.slider(
        "Importance of public services per capita",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = preference for countries with more public services"
    )
    
    # Get recommendations button
    recommend_button = st.button("Find Best Countries 🌍", type="primary", use_container_width=True)

# Main content area
if recommend_button:
    with st.spinner("Finding your ideal EU countries..."):
        recommendations = get_recommendations(preferences)
    
    if recommendations:
        st.success("Successfully personalized your recommendations!")
        
        # Display top recommendations
        top_countries = recommendations['recommendations'][:5]
        
        # TABS
        tab1, tab2, tab3 = st.tabs(["↥ Top Recommendations", "⏀ Comparison Chart", "⊙ All Results"])
        
        with tab1:
            st.subheader("Your Top 5 Countries")
            
            for i, country in enumerate(top_countries):
                with st.expander(f"#{i+1} {country['country']} - Match Score: {country['similarity_score']:.1%}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Weekly Hours", f"{country['weekly_hours']:.1f} hrs")
                        st.metric("Cash Support", f"€{country['cash_per_capita']:,.0f}")
                    
                    with col2:
                        st.metric("Maternity Support", f"€{country['maternity_per_capita']:,.0f}")
                        st.metric("Public Services", f"€{country['services_per_capita']:,.0f}")
                    
                    # maybe: add radarr chart...
                    fig = create_radar_chart(country, preferences)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.divider()

                    # extra info
                    col1, col2 = st.columns(2)
                    with col1:
                        if country['birth_rate_per_thousand']:
                            st.metric(f"Birth Rate of {country['country']}", f"{country['birth_rate_per_thousand']:.1f} per 1000")
                    with col2:
                        if country['price_index']:
                            st.metric(f"Consumer Price Index of {country['country']}", f"{country['price_index']:.1f}")
                    st.caption(f"Data from year: {country['year']}")
        
        with tab2:
            st.subheader("Country Comparison")
            
            # Create comparison dataframe
            df_compare = pd.DataFrame(top_countries)
            
            # Bar chart for similarity scores
            fig_similarity = px.bar(
                df_compare,
                x='country',
                y='similarity_score',
                title='Match Scores by Country',
                labels={'similarity_score': 'Match Score', 'country': 'Country'},
                color='similarity_score',
                color_continuous_scale='Blues'
            )

            # update bar
            fig_similarity.update_traces(text=[f"{x:.1%}" for x in df_compare['similarity_score']], textposition='outside')
            st.plotly_chart(fig_similarity, use_container_width=True)

            st.divider()
            
            # Comparison of features
            features_to_compare = ['weekly_hours', 'cash_per_capita', 'maternity_per_capita', 'services_per_capita']
            df_features = df_compare[['country'] + features_to_compare].melt(
                id_vars=['country'],
                var_name='Feature',
                value_name='Value'
            )
            
            fig_features = px.bar(
                df_features,
                x='country',
                y='Value',
                color='Feature',
                title='Feature Comparison Across Top Countries',
                barmode='group'
            )

            fig_features.update_layout(
                yaxis_type='log',
                yaxis_title='Value (Log Scale)',
                xaxis_title='EU Country'
            )
            st.plotly_chart(fig_features, use_container_width=True)
        
        with tab3:
            st.subheader("All Country Rankings")
            
            # FULL dataframe
            df_all = pd.DataFrame(recommendations['recommendations'])
            
            # format columns
            df_display = df_all[['country', 'similarity_score', 'weekly_hours', 
                                'cash_per_capita', 'maternity_per_capita', 'services_per_capita', 'year']].copy()
            
            df_display.columns = ['Country', 'Match Score', 'Weekly Hours', 
                                'Cash Support (€)', 'Maternity Support (€)', 'Public Services (€)', 'Data Year']
            
            # FORMAT?? Nurmic columns
            df_display['Match Score'] = df_display['Match Score'].apply(lambda x: f"{x:.1%}")
            df_display['Weekly Hours'] = df_display['Weekly Hours'].apply(lambda x: f"{x:.1f}")
            df_display['Cash Support (€)'] = df_display['Cash Support (€)'].apply(lambda x: f"{x:,.0f}")
            df_display['Maternity Support (€)'] = df_display['Maternity Support (€)'].apply(lambda x: f"{x:,.0f}")
            df_display['Public Services (€)'] = df_display['Public Services (€)'].apply(lambda x: f"{x:,.0f}")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            st.caption("Note: Table is resizable.")

            st.divider()

            # Map visualization
            loc_col  = 'iso_code'     if 'iso_code'  in df_all.columns else 'country'
            loc_mode = 'ISO-3'        if loc_col == 'iso_code'        else 'country names'
        
            if 'iso_code' in df_all.columns or 'country_code' in df_all.columns:
                fig_map = px.choropleth(
                    df_all,
                    locations=loc_col,
                    locationmode=loc_mode,
                    color='similarity_score',
                    hover_name='country',
                    color_continuous_scale='Blues',
                    range_color=(0, 1),
                    scope='europe',
                    title='EU Countries by Match Score',
                    width=950,
                    height=700,
                )
                fig_map.update_geos(fitbounds="locations", visible=False)

                fig_map.update_layout(
                    title_font=dict(size=30),   # bigger title
                    margin=dict(l=0, r=0, t=80, b=0)            # t=80 gives head-room for the title
                )

                st.plotly_chart(fig_map, use_container_width=True)

else: # no recs just yet
    # Show instructions
    st.info("← Use the sliders in the sidebar to set your preferences, then click 'Find Best Countries.'")

    st.divider()

    stats = get_feature_stats()

    if stats:
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
        
        st.divider()

        st.markdown("### Feature Ranges Across EU Countries")
        
        feature_names = {
            'weekly_hours': 'Weekly Hours',
            'cash_per_capita': 'Cash Support (€)',
            'maternity_per_capita': 'Maternity Support (€)',
            'services_per_capita': 'Public Services (€)'
        }
        
        for feature, display_name in feature_names.items():
            if feature in stats['statistics']:
                stat = stats['statistics'][feature]
                col1, col2, col3, col4 = st.columns(4)
                col1.metric(f"{display_name} - Min", f"{stat['min']:,.0f}")
                col2.metric("Average", f"{stat['mean']:,.0f}")
                col3.metric("Median", f"{stat['median']:,.0f}")
                col4.metric("Max", f"{stat['max']:,.0f}")


st.sidebar.divider()
AlwaysShowAtBottom()
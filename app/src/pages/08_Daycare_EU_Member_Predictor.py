import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
from modules.nav import SideBarLinks, AlwaysShowAtBottom

# Page configuration
st.set_page_config(
    page_title="EU Country Recommender",
    page_icon="🇪🇺",
    layout="wide"
)

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Configuration
API_BASE_URL = "http://web-api:4000/model2"  # Adjust based on your Flask server URL

# Custom CSS
st.markdown("""
<style>
    .recommendation-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_feature_stats() -> Dict:
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

def get_recommendations(preferences: Dict) -> Dict:
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

def create_radar_chart(country_data: Dict, user_prefs: Dict) -> go.Figure:
    """Create a radar chart comparing country features with user preferences"""
    categories = ['Weekly Hours', 'Cash Support', 'Maternity Support', 'Services']
    
    # Normalize country values to 0-10 scale for comparison
    # This is a simplified normalization - in production, you'd use the actual min/max from all countries
    country_values = [
        10 - (country_data.get('weekly_hours', 40) - 29) / (41 - 29) * 10,  # Inverted: lower hours = higher score
        country_data.get('cash_per_capita', 0) / 50000 * 10,  # Assuming max ~50k
        country_data.get('maternity_per_capita', 0) / 1000 * 10,  # Assuming max ~1k
        country_data.get('services_per_capita', 0) / 50000 * 10  # Assuming max ~50k
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
        height=400
    )
    
    return fig

# Main app
def main():
    st.title("🇪🇺 EU Country Recommender")
    st.markdown("Find the EU country that best matches your preferences for work-life balance and family support!")
    
    # Sidebar for user preferences
    with st.sidebar:
        st.header("Your Preferences")
        st.markdown("Rate the importance of each factor from 0 (not important) to 10 (very important)")
        
        preferences = {}
        
        # Weekly Hours slider
        st.subheader("💼 Work-Life Balance")
        preferences['weekly_hours'] = st.slider(
            "Preference for shorter working hours",
            min_value=0,
            max_value=10,
            value=5,
            help="Higher value = preference for countries with shorter working weeks"
        )
        
        # Cash Support slider
        st.subheader("💰 Cash Support")
        preferences['cash_per_capita'] = st.slider(
            "Importance of cash benefits per capita",
            min_value=0,
            max_value=10,
            value=5,
            help="Higher value = preference for countries with more cash support"
        )
        
        # Maternity Support slider
        st.subheader("👶 Maternity Support")
        preferences['maternity_per_capita'] = st.slider(
            "Importance of maternity benefits",
            min_value=0,
            max_value=10,
            value=5,
            help="Higher value = preference for countries with better maternity support"
        )
        
        # Services Support slider
        st.subheader("🏥 Public Services")
        preferences['services_per_capita'] = st.slider(
            "Importance of public services per capita",
            min_value=0,
            max_value=10,
            value=5,
            help="Higher value = preference for countries with more public services"
        )
        
        # Get recommendations button
        recommend_button = st.button("🔍 Find Best Countries", type="primary", use_container_width=True)
    
    # Main content area
    if recommend_button:
        with st.spinner("Finding your ideal EU countries..."):
            recommendations = get_recommendations(preferences)
        
        if recommendations:
            st.success("Here are your personalized recommendations!")
            
            # Display top recommendations
            top_countries = recommendations['recommendations'][:5]
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["🏆 Top Recommendations", "📊 Comparison Chart", "📈 All Results"])
            
            with tab1:
                st.subheader("Top 5 Countries for You")
                
                for i, country in enumerate(top_countries):
                    with st.expander(f"#{i+1} {country['country']} - Match Score: {country['similarity_score']:.1%}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Weekly Hours", f"{country['weekly_hours']:.1f} hrs")
                            st.metric("Cash Support", f"€{country['cash_per_capita']:,.0f}")
                        
                        with col2:
                            st.metric("Maternity Support", f"€{country['maternity_per_capita']:,.0f}")
                            st.metric("Public Services", f"€{country['services_per_capita']:,.0f}")
                        
                        # Add radar chart
                        fig = create_radar_chart(country, preferences)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Additional info
                        if country['birth_rate_per_thousand']:
                            st.info(f"Birth Rate: {country['birth_rate_per_thousand']:.1f} per 1000")
                        if country['price_index']:
                            st.info(f"Price Index: {country['price_index']:.1f}")
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
                fig_similarity.update_traces(text=[f"{x:.1%}" for x in df_compare['similarity_score']], textposition='outside')
                st.plotly_chart(fig_similarity, use_container_width=True)
                
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
                st.plotly_chart(fig_features, use_container_width=True)
            
            with tab3:
                st.subheader("All Country Rankings")
                
                # Create full dataframe
                df_all = pd.DataFrame(recommendations['recommendations'])
                
                # Format columns
                df_display = df_all[['country', 'similarity_score', 'weekly_hours', 
                                   'cash_per_capita', 'maternity_per_capita', 'services_per_capita', 'year']].copy()
                
                df_display.columns = ['Country', 'Match Score', 'Weekly Hours', 
                                    'Cash Support (€)', 'Maternity Support (€)', 'Public Services (€)', 'Data Year']
                
                # Format numeric columns
                df_display['Match Score'] = df_display['Match Score'].apply(lambda x: f"{x:.1%}")
                df_display['Weekly Hours'] = df_display['Weekly Hours'].apply(lambda x: f"{x:.1f}")
                df_display['Cash Support (€)'] = df_display['Cash Support (€)'].apply(lambda x: f"{x:,.0f}")
                df_display['Maternity Support (€)'] = df_display['Maternity Support (€)'].apply(lambda x: f"{x:,.0f}")
                df_display['Public Services (€)'] = df_display['Public Services (€)'].apply(lambda x: f"{x:,.0f}")
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                # Map visualization
                if 'iso_code' in df_all.columns or 'country_code' in df_all.columns:
                    fig_map = px.choropleth(
                        df_all,
                        locations='country_code',
                        locationmode='ISO-3' if 'iso_code' in df_all.columns else 'country names',
                        color='similarity_score',
                        hover_name='country',
                        color_continuous_scale='Blues',
                        range_color=(0, 1),
                        scope='europe',
                        title='EU Countries by Match Score'
                    )
                    fig_map.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig_map, use_container_width=True)
    
    else:
        # Show instructions when no recommendations yet
        st.info("👈 Use the sliders in the sidebar to set your preferences, then click 'Find Best Countries'")
        
        # Show feature statistics
        with st.expander("📊 Learn About the Features"):
            stats = get_feature_stats()
            if stats:
                st.markdown("### What do these features mean?")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **💼 Weekly Hours**: Average working hours per week. Lower is generally better for work-life balance.
                    
                    **💰 Cash Support**: Government cash benefits per capita (in EUR). Higher means more financial support.
                    """)
                
                with col2:
                    st.markdown("""
                    **👶 Maternity Support**: Maternity benefits per capita (in EUR). Higher means better parental support.
                    
                    **🏥 Public Services**: Public services spending per capita (in EUR). Higher means better public services.
                    """)
                
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

if __name__ == "__main__":
    main()


st.sidebar.divider()
AlwaysShowAtBottom()
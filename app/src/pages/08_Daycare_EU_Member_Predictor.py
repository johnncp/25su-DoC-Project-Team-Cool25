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
API_BASE_URL = "http://web-api:4000/model2" 

Back("00_Daycare_Home.py")

# Helper functions
# Fetch feature stats from API
def get_feature_stats() -> Dict: # return Dict
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

# Get country recs
def get_recommendations(preferences: Dict) -> Dict: # returh Dict
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


# Create radar charts
def create_radar_chart(country_data: Dict, user_prefs: Dict) -> go.Figure: # return go Figure
    categories = ['Work-Life Balance', 'Parent Cash Benefits', 'Maternity Support', 'Public Childcare']
    
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
        name='Country Market',
        line_color='blue'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=user_values,
        theta=categories,
        fill='toself',
        name='Your Business Priorities',
        line_color='red'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        height=500,
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
        transform: translate(-60%, -80%);
        color: #31333E;
        font-size: 3.8rem;
        font-weight: bold;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        padding: 15px 25px;
        border-radius: 8px;
        opacity: 0;
        max-width: 60vw;          /* enough room for two long lines            */
        white-space: nowrap;      /* default; keeps natural wrapping behaviour */
        line-height: 0.8;           /* a little more vertical space than 0.8     */
        animation: fadeIn 0.5s ease-out forwards;
    }}
    </style>

    <img src="data:image/png;base64,{background_img}">
    <div class="overlay-text">🏢 EU Market Expansion Advisor</div>
""", unsafe_allow_html=True)

st.markdown("Find the best EU countries for expanding your daycare business based on market conditions and government support!")

# Sidebar for user preferences
with st.sidebar:
    st.header("Business Priorities 》")
    st.markdown("Rate from **0** (not important) to **10** (very important) for your expansion strategy.")
    
    preferences = {}
    
    # Weekly Hours slider
    st.subheader("Parent Work-Life Balance 👨‍👩‍👧")
    preferences['weekly_hours'] = st.slider(
        "Target markets with work-life balance needs",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = prioritize countries where parents work fewer hours and may need flexible daycare options"
    )
    
    # Cash Support slider
    st.subheader("Parent Purchasing Power 💸")
    preferences['cash_per_capita'] = st.slider(
        "Importance of parent cash benefits",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = prioritize countries where parents receive more cash benefits (higher ability to pay for daycare)"
    )
    
    # Maternity Support slider
    st.subheader("Maternity Market Size 🍼")
    preferences['maternity_per_capita'] = st.slider(
        "Importance of maternity support levels",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = prioritize countries with strong maternity support (indicating family-friendly policies and potential demand)"
    )
    
    # Services Support slider
    st.subheader("Public Childcare Competition 🏛️")
    preferences['services_per_capita'] = st.slider(
        "Consider public childcare services",
        min_value=0,
        max_value=10,
        value=5,
        help="Higher value = prioritize countries with more public services (Note: may indicate more competition from public daycare)"
    )
    
    # Get recommendations button
    recommend_button = st.button("Find Best Markets", type="primary", use_container_width=True)
    if recommend_button:
        with st.spinner("Fiddling..."):
            time.sleep(1)

# Main content area
if recommend_button:
    with st.spinner("Analyzing EU markets for daycare expansion opportunities..."):
        recommendations = get_recommendations(preferences)
    
    if recommendations:
        st.success("Market analysis complete. Your top expansion opportunities are:")
        
        # Display top recommendations
        top_countries = recommendations['recommendations'][:5]
        
        # TABS
        tab1, tab2, tab3, tab4 = st.tabs(["↥ Top Markets", "♘ Market Comparison", "⊙ Full Analysis", "☰ From The News"])
        
        with tab1:
            st.subheader("Top 5 Markets for Daycare Expansion")
            
            for i, country in enumerate(top_countries):
                with st.expander(f"#{i+1} {country['country']} - Market Fit Score: {country['similarity_score']:.1%}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Avg. Parent Work Week", f"{country['weekly_hours']:.1f} hrs", 
                                help="Lower hours may indicate higher demand for flexible daycare")
                        st.metric("Parent Cash Benefits", f"€{country['cash_per_capita']:,.0f}/year", 
                                help="Higher benefits = greater ability to pay for private daycare")
                    
                    with col2:
                        st.metric("Maternity Benefits", f"€{country['maternity_per_capita']:,.0f}", 
                                help="Strong maternity support indicates family-friendly market")
                        st.metric("Public Childcare Spending", f"€{country['services_per_capita']:,.0f}", 
                                help="Consider competition from public daycare services")
                    
                    # Market analysis chart
                    fig = create_radar_chart(country, preferences)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.divider()

                    # Market indicators
                    col1, col2 = st.columns(2)
                    with col1:
                        if country['birth_rate_per_thousand']:
                            st.metric(f"Birth Rate", f"{country['birth_rate_per_thousand']:.1f} per 1000", 
                                    help="Higher birth rate = larger potential customer base")
                    with col2:
                        if country['price_index']:
                            st.metric(f"Cost of Living Index", f"{country['price_index']:.1f}", 
                                    help="Consider operational costs in this market")
                    
                    # Business insights
                    st.info(f"""
                    **Market Insights for {country['country']}:**
                    - Parent purchasing power: €{country['cash_per_capita']:,.0f} in government support
                    - Work-life balance: {country['weekly_hours']:.1f} hour work week
                    - Family support infrastructure: {'Strong' if country['maternity_per_capita'] > 500 else 'Moderate' if country['maternity_per_capita'] > 100 else 'Limited'}
                    - Competition level: {'High' if country['services_per_capita'] > 50000 else 'Moderate' if country['services_per_capita'] > 20000 else 'Low'} public childcare investment
                    """)
                    
                    st.caption(f"Market data from: {country['year']}")
        
        with tab2:
            st.subheader("Market Comparison Analysis")
            
            # Create comparison dataframe
            df_compare = pd.DataFrame(top_countries)
            
            # Bar chart for similarity scores
            fig_similarity = px.bar(
                df_compare,
                x='country',
                y='similarity_score',
                title='Market Fit Scores by Country',
                labels={'similarity_score': 'Market Fit Score', 'country': 'Country'},
                color='similarity_score',
                color_continuous_scale='Greens'
            )

            # update bar
            fig_similarity.update_traces(text=[f"{x:.1%}" for x in df_compare['similarity_score']], textposition='outside')
            st.plotly_chart(fig_similarity, use_container_width=True)

            st.divider()
            
            # Market factors comparison
            features_to_compare = ['weekly_hours', 'cash_per_capita', 'maternity_per_capita', 'services_per_capita']
            
            # Create custom labels for business context
            feature_labels = {
                'weekly_hours': 'Work Week (hrs)',
                'cash_per_capita': 'Parent Cash Benefits (€)',
                'maternity_per_capita': 'Maternity Support (€)',
                'services_per_capita': 'Public Childcare (€)'
            }
            
            df_features = df_compare[['country'] + features_to_compare].copy()
            df_features = df_features.rename(columns=feature_labels)
            
            df_features_melted = df_features.melt(
                id_vars=['country'],
                var_name='Market Factor',
                value_name='Value'
            )
            
            fig_features = px.bar(
                df_features_melted,
                x='country',
                y='Value',
                color='Market Factor',
                title='Key Market Factors Comparison',
                barmode='group'
            )

            fig_features.update_layout(
                yaxis_type='log',
                yaxis_title='Value (Log Scale)',
                xaxis_title='Target Markets'
            )
            st.plotly_chart(fig_features, use_container_width=True)
        
        with tab3:
            st.subheader("Complete Market Analysis")
            
            # FULL dataframe
            df_all = pd.DataFrame(recommendations['recommendations'])
            
            # format columns
            df_display = df_all[['country', 'similarity_score', 'weekly_hours', 
                                'cash_per_capita', 'maternity_per_capita', 'services_per_capita', 'year']].copy()
            
            df_display.columns = ['Market', 'Fit Score', 'Work Week (hrs)', 
                                'Parent Benefits (€)', 'Maternity Support (€)', 'Public Childcare (€)', 'Data Year']
            
            # FORMAT Numeric columns
            df_display['Fit Score'] = df_display['Fit Score'].apply(lambda x: f"{x:.1%}")
            df_display['Work Week (hrs)'] = df_display['Work Week (hrs)'].apply(lambda x: f"{x:.1f}")
            df_display['Parent Benefits (€)'] = df_display['Parent Benefits (€)'].apply(lambda x: f"{x:,.0f}")
            df_display['Maternity Support (€)'] = df_display['Maternity Support (€)'].apply(lambda x: f"{x:,.0f}")
            df_display['Public Childcare (€)'] = df_display['Public Childcare (€)'].apply(lambda x: f"{x:,.0f}")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            st.caption("💡 Tip: Click column headers to sort. Consider both market fit and competition levels.")

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
                    color_continuous_scale='Greens',
                    range_color=(0, 1),
                    scope='europe',
                    title='EU Daycare Market Opportunities',
                    width=950,
                    height=700,
                )
                fig_map.update_geos(fitbounds="locations", visible=False)

                fig_map.update_layout(
                    title_font=dict(size=30),
                    margin=dict(l=0, r=0, t=80, b=0)
                )

                st.plotly_chart(fig_map, use_container_width=True)
        
        with tab4:
            API_KEY = 'b7fbb637b8044d34b684ae6076ee98e2'
            DEFAULT_TOPIC = "European Union Daycare"
            user_topic = DEFAULT_TOPIC

            # Display
            st.header(f"The Latest News on {user_topic}")

            # Text input from user
            user_topic = st.text_input("Or click to refine queries yourself:", value=DEFAULT_TOPIC)

            # Disclaimer
            st.caption("• Eurobébé is not affiliated with the following articles and does not confirm factuality. Use intended for informational purposes only.")

            # Request to NewsAPI
            url = f"https://newsapi.org/v2/everything?q={user_topic}&sortBy=publishedAt&language=en&apiKey={API_KEY}"

            # Fetch
            response = requests.get(url)
            data = response.json()

            if data.get("articles"):
                articles = data["articles"][:6]  # Top 6

                # Create 3 columns
                cols = st.columns(3)

                for i, article in enumerate(articles):
                    with cols[i % 3]:
                        st.markdown(
                            f"""
                            <div style="border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:10px; background-color:#F4F4F4;">
                                <img src="{article['urlToImage']}" style="width:100%; border-radius:8px; margin-bottom:10px;" />
                                <h4 style="margin-top:0;">{article['title']}</h4>
                                <p>{article['description'] or ''}</p>
                                <a href="{article['url']}" target="_blank">Read more</a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.warning("No articles found. Try a different topic.")

else: # no recs just yet
    # Show instructions
    st.info("← Use the sliders to set your business priorities, then click 'Find Best Markets' to see expansion opportunities.")

    st.divider()

    stats = get_feature_stats()

    if stats:
        st.markdown("### Understanding Market Factors for Daycare Expansion")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **👨‍👩‍👧 Parent Work-Life Balance**: Average working hours per week. Countries with shorter work weeks may have higher demand for flexible daycare options, while longer hours indicate need for extended daycare services.
            
            **💸 Parent Purchasing Power**: Government cash benefits per capita (€). Higher benefits mean parents have more disposable income to spend on quality private daycare services.
            """)
        
        with col2:
            st.markdown("""
            **🍼 Maternity Market Indicators**: Maternity benefits per capita (€). Strong maternity support indicates a family-friendly market with potential for premium daycare services.
            
            **🏛️ Public Competition**: Public childcare spending per capita (€). Higher spending may mean more competition from subsidized options, but also indicates strong childcare infrastructure and demand.
            """)
        
        st.divider()

        st.markdown("### Market Ranges Across EU Countries")
        st.caption("Use these ranges to understand the market landscape:")
        
        feature_names = {
            'weekly_hours': 'Work Week Range',
            'cash_per_capita': 'Parent Benefits Range (€)',
            'maternity_per_capita': 'Maternity Support Range (€)',
            'services_per_capita': 'Public Childcare Range (€)'
        }
        
        for feature, display_name in feature_names.items():
            if feature in stats['statistics']:
                stat = stats['statistics'][feature]
                col1, col2, col3, col4 = st.columns(4)
                col1.metric(f"Minimum", f"{stat['min']:,.0f}")
                col2.metric("EU Average", f"{stat['mean']:,.0f}")
                col3.metric("EU Median", f"{stat['median']:,.0f}")
                col4.metric("Maximum", f"{stat['max']:,.0f}")
    


st.sidebar.divider()
AlwaysShowAtBottom()
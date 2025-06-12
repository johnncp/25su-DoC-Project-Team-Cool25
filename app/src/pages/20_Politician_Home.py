import logging
logger = logging.getLogger(__name__)
import base64, requests

import streamlit as st
from modules.nav import SideBarLinks, AlwaysShowAtBottom
import requests

API_KEY = 'b7fbb637b8044d34b684ae6076ee98e2'
DEFAULT_TOPIC = "European Union Birth Rates"
user_topic = DEFAULT_TOPIC

st.set_page_config(layout = 'wide')

SideBarLinks()
AlwaysShowAtBottom()

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

background_img = get_base64("assets/20_Politician/politician_home_background.png")

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
        transform: translate(-100%, -120%);
        color: #31333E;
        font-size: 4.2rem;
        font-weight: bold;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        padding: 15px 25px;
        border-radius: 8px;
        line-height: 0.8;
        opacity: 0;
        animation: fadeIn 0.5s ease-out forwards;
    }}

    .subheading {{
        position: absolute;
        top: 60%;
        left: 50%;
        transform: translate(-100%, -120%);
        color: #31333E;
        font-size: 1.6rem;
        font-weight: 400;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.05);
        padding: 10px 25px;
        border-radius: 8px;
        line-height: 1;
        opacity: 0;
        animation: fadeIn 0.5s ease-out forwards;
    }}
    </style>

    <img src="data:image/png;base64,{background_img}">
    <div class="overlay-text">Welcome, {st.session_state['first_name']}!</div>
    <div class="subheading">Continue your work for the community. For the region. For the world.</div>
""", unsafe_allow_html=True)

# Display
st.title(f"The Latest News on {user_topic}")

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

st.divider()

st.title(f"Be the change, {st.session_state['first_name']}.")

# Nav to features
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('〰️ Birth Rate Predictor', type='primary', use_container_width=True):
        st.success("Redirecting to Model..."),
        st.switch_page('pages/21_Politician_Birth_Rate_Predictor.py')

with col2:
    if st.button('🔎 Legislation Finder', type='primary', use_container_width=True):
        st.success("Legendary sessions..."),
        st.switch_page('pages/22_Politician_Legislation_Finder.py')

with col3:
    if st.button('☰ Resource Page', type='primary', use_container_width=True):
        #st.write("Page coming soon!")
        #st.success("Redirecting to Resources..."),
        st.switch_page('pages/24_Politician_Resources.py')

st.divider()
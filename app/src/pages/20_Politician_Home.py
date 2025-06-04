import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

API_KEY = 'b7fbb637b8044d34b684ae6076ee98e2'
DEFAULT_TOPIC = "European birth rates"
user_topic = DEFAULT_TOPIC

# Display
st.title(f"Latest News on {user_topic}")

# Text input from user
user_topic = st.text_input("Or refine yourself:", value=DEFAULT_TOPIC)

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

if st.button('Update ML Models', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Birth_Rate_Predictor.py')
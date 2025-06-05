import logging
import base64, requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

background_img = get_base64("assets/caraday_home_background.png")

st.markdown(f"""
    <style>
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
    }}
    </style>

    <img src="data:image/png;base64,{background_img}">
        <div class="overlay-text">Welcome, {st.session_state['first_name']}!</div>
        <div class="subheading">What can we do for your daycare today?</div>
""", unsafe_allow_html=True)

# Nav to features
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('☆ Predict an EU Member', type='primary', use_container_width=True):
        st.success("Redirecting to Country Predictor..."),
        st.switch_page('pages/01_EU_Member_Predictor.py')

with col2:
    if st.button('☰ Resource Page', type='primary', use_container_width=True):
        st.success("Redirecting to Resources..."),
        st.switch_page('pages/02_Daycare_Resources.py')

with col3:
    if st.button('⏱︎ Operating Hours', type='primary', use_container_width=True):
        st.success("Opening hours section..."),
        st.switch_page('pages/03_Operating_Hours.py')
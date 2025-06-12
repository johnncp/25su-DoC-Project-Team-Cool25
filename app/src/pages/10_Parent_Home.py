import logging
import base64, requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks, AlwaysShowAtBottom

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
AlwaysShowAtBottom()

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

background_img = get_base64("assets/10_Parent_Home/parent_home_background.png")

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
    <div class="overlay-text">Hey there, {st.session_state['first_name']}!</div>
    <div class="subheading">We're here for you to take highly informed steps in life.</div>
""", unsafe_allow_html=True)

st.title(f"Choose your research.")

# Nav to features
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('☆ Find Countries by Childcare Spending', type='primary', use_container_width=True):
        st.success("Redirecting to EU predictor..."),
        st.switch_page('pages/11_Parent_EU_Member_Predictor.py')

with col2:
    if st.button('🔎 Daycare Finder', type='primary', use_container_width=True):
        st.success("Legendary sessions..."),
        st.switch_page('pages/02_Daycare_Resources.py')

with col3:
    if st.button('☰ Resource Page', type='primary', use_container_width=True):
        st.success("Redirecting to Resources..."),
        st.switch_page('pages/17_Parent_Affinity_Resources.py')

st.divider()
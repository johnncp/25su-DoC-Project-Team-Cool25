import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome USAID Worker, {st.session_state['first_name']}.")
st.write('')

# Nav to features
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('⊙ EU Member Predictor', type='primary', use_container_width=True):
        st.success("Redirecting to EU predictor..."),
        st.switch_page('pages/11_Birth_Rate_predicte.py')

with col2:
    if st.button('🔎 Legislation Finder', type='primary', use_container_width=True):
        st.success("Legendary sessions..."),
        st.switch_page('pages/22_Legislation_Finder.py')

with col3:
    if st.button('☰ Resource Page', type='primary', use_container_width=True):
        st.success("Redirecting to Resources..."),
        st.switch_page('pages/23_Family_Time_Resources.py')

st.divider()

st.write('')
st.write('### What would you like to do today?')

if st.button('Predict Value Based on Regression Model', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Prediction.py')

if st.button('View the Simple API Demo', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_API_Test.py')

if st.button("View Classification Demo",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Classification.py')
  
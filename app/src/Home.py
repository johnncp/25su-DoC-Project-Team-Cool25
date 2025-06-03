##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
import base64
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading Eurobébé Home...")

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

background_img = get_base64("assets/homepage_background.png")

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
        <div class="overlay-text">Welcome to Eurobébé</div>
        <div class="subheading">Discover Europe's Preferred Resource for Parenthood.</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("<h2 style='text-align: center;'>Are you here as...</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("# A daycare?")
    st.write('Also a good match for:')
    st.markdown(
        """
        :primary-badge[After-School Programs] :primary-badge[Montessori School Operators]
        :primary-badge[Preschool Owners] :primary-badge[Nonprofit Child Advocacies]
        """
        )
    if st.button("Log in as Cara Day", 
            type = 'primary', 
            use_container_width=True):
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'daycare_operator'
        # we add the first name of the user (so it can be displayed on 
        # subsequent pages). 
        st.session_state['first_name'] = 'Cara'
        # finally, we ask streamlit to switch to another page, in this case, the 
        # landing page for this particular user type
        logger.info("Logging in as Daycare Operator Cara Day")
        st.switch_page('pages/00_Pol_Strat_Home.py')

with col2:
    st.markdown("# A parent?")
    st.write('Also a good match for:')
    st.markdown(
        """
        :primary-badge[Adoptive Parents] :primary-badge[Caregivers]
        :primary-badge[PTA Members] :primary-badge[Homeschooling]
        :primary-badge[Suburban Parents] :primary-badge[Family Support Group Members]
        """
        )
    if st.button("Log in as Eura Pean", 
            type = 'primary', 
            use_container_width=True):
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'parent'
        # we add the first name of the user (so it can be displayed on 
        # subsequent pages). 
        st.session_state['first_name'] = 'Eura'
        # finally, we ask streamlit to switch to another page, in this case, the 
        # landing page for this particular user type
        logger.info("Logging in as Parent Eura Pean")
        st.switch_page('pages/10_USAID_Worker_Home.py')

with col3:
    st.markdown("# A politician?")
    st.write('Also a good match for:')
    st.markdown(
        """
        :primary-badge[Senators] :primary-badge[County Commissioners]
        :primary-badge[Political Strategists] :primary-badge[Political Influencer]
        :primary-badge[Lobbyists]
        """
        )
    if st.button("Log in as Paul E. Tishan", 
            type = 'primary', 
            use_container_width=True):
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'politician'
        # we add the first name of the user (so it can be displayed on 
        # subsequent pages). 
        st.session_state['first_name'] = 'Paul'
        # finally, we ask streamlit to switch to another page, in this case, the 
        # landing page for this particular user type
        logger.info("Logging in as Politician Paul E. Tishan")
        st.switch_page('pages/20_Admin_Home.py')

st.divider()
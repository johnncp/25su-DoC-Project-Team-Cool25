##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging, requests
import base64
from streamlit.components.v1 import html
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
    
def fetch_users_by_role(role_id):
    try:
        response = requests.get(f"http://web-api:4000/users/role/{role_id}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching users: {e}")

background_img = get_base64("assets/homepage_background.png")

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
        font-size: 3.8rem;
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
        transform: translate(-100%, -95%);
        color: #31333E;
        font-size: 1.2rem;
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
    <div class="overlay-text">Welcome to Eurobébé</div>
    <div class="subheading">Discover Europe's Preferred Resource for Parenthood. A CS 4973 Project at Northeastern University.</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("<h2 style='text-align: center;'>Are you here as...</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Fetch users, going by role
daycare_users = fetch_users_by_role(1)  # role_id 1: daycare
parent_users = fetch_users_by_role(2)   # role_id 2: parent
politician_users = fetch_users_by_role(3)  # role_id 3: politician

with col1:
    st.markdown("# A daycare?")
    st.write('Also a good match for:')
    st.markdown(
        """
        :primary-badge[After-School Programs] :primary-badge[Montessori School Operators]
        :primary-badge[Preschool Owners] :primary-badge[Nonprofit Child Advocacies]
        """
    )
    
    # Create dropdown with daycare users
    if daycare_users:
        daycare_options = {f"{user['first_name']} {user['last_name']}": user for user in daycare_users}
        selected_daycare = st.selectbox(
            "Select a daycare operator:",
            options=list(daycare_options.keys()),
            key="daycare_select"
        )
        
        if st.button(f"Log in as {selected_daycare}", 
                type='primary', 
                icon=":material/login:",
                use_container_width=True,
                key="daycare_login"):
            selected_user = daycare_options[selected_daycare]

            # Clear any existing user-specific notes from session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith("notes_")]
            for key in keys_to_remove:
                del st.session_state[key]

            st.session_state['authenticated'] = True
            st.session_state['role'] = 'daycare_operator'
            st.session_state['first_name'] = selected_user['first_name']
            st.session_state['user_id'] = selected_user['user_id']
            logger.info(f"Logging in as Daycare Operator {selected_daycare}")
            st.switch_page('pages/00_Daycare_Home.py')
    else:
        st.error("No daycare operators available.")

with col2:
    st.markdown("# A parent?")
    st.write('Also a good match for:')
    st.markdown(
        """
        :primary-badge[Adoptive Parents] :primary-badge[Caregivers]
        :primary-badge[PTA Members] :primary-badge[Homeschools]
        :primary-badge[Suburban Parents] :primary-badge[Family Support Group Members]
        """
    )
    
    # Create dropdown with parent users
    if parent_users:
        parent_options = {f"{user['first_name']} {user['last_name']}": user for user in parent_users}
        selected_parent = st.selectbox(
            "Select a parent:",
            options=list(parent_options.keys()),
            key="parent_select"
        )
        
        if st.button(f"Log in as {selected_parent}", 
                type='primary', 
                icon=":material/login:",
                use_container_width=True,
                key="parent_login"):
            selected_user = parent_options[selected_parent]

            # Clear any existing user-specific notes from session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith("notes_")]
            for key in keys_to_remove:
                del st.session_state[key]

            st.session_state['authenticated'] = True
            st.session_state['role'] = 'parent'
            st.session_state['first_name'] = selected_user['first_name']
            st.session_state['user_id'] = selected_user['user_id']
            logger.info(f"Logging in as Parent {selected_parent}")
            st.switch_page('pages/10_Parent_Home.py')
    else:
        st.error("No parents available")

with col3:
    st.markdown("# A politician?")
    st.write('Also a good match for:')
    st.markdown(
        """
        :primary-badge[Senators] :primary-badge[County Commissioners]
        :primary-badge[Political Strategists] :primary-badge[Political Influencers]
        :primary-badge[Lobbyists]
        """
    )
    
    # Create dropdown with politician users
    if politician_users:
        politician_options = {f"{user['first_name']} {user['last_name']}": user for user in politician_users}
        selected_politician = st.selectbox(
            "Select a politician:",
            options=list(politician_options.keys()),
            key="politician_select"
        )
        
        if st.button(f"Log in as {selected_politician}", 
                type='primary', 
                icon=":material/login:",
                use_container_width=True,
                key="politician_login"):
            selected_user = politician_options[selected_politician]

            # Clear any existing user-specific notes from session state
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith("notes_")]
            for key in keys_to_remove:
                del st.session_state[key]

            st.session_state['authenticated'] = True
            st.session_state['role'] = 'politician'
            st.session_state['first_name'] = selected_user['first_name']
            st.session_state['user_id'] = selected_user['user_id']
            logger.info(f"Logging in as Politician {selected_politician}")
            st.switch_page('pages/20_Politician_Home.py')
    else:
        st.error("No politicians available")

st.divider()

carousel_image_paths = [
    "assets/Home/carousel_1.jpg",
    "assets/Home/carousel_2.jpg",
    "assets/Home/carousel_3.jpg",
    "assets/Home/carousel_4.jpg"
]

# Create the HTML string of images
img_tags = ""
for path in carousel_image_paths:
    img_b64 = get_base64(path)
    img_tags += f'<img src="data:image/jpeg;base64,{img_b64}" alt="local image">'

carousel_html = f"""
<style>
.carousel-wrapper {{
    position: relative;
    width: auto;
    height: 400px;
    overflow: hidden;
}}

.white-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background: linear-gradient(to top, rgba(255,255,255,1), rgba(255,255,255,.25));
    z-index: 1;
    pointer-events: none;
}}

.carousel-track {{
    display: flex;
    animation: scroll 30s linear infinite;
    width: max-content;
    z-index: 0;
}}

.carousel-track img {{
    width: auto;
    height: 150%;
    object-fit: cover;
    margin-right: 10px;
}}

/* Overlay Text */
.carousel-overlay {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: #31333E;
    z-index: 2;
    pointer-events: none;
    font-family: 'Segoe UI', sans-serif;
    width: 80%;
    max-width: 1000px;
}}

.carousel-overlay h1 {{
    font-size: 3.8rem;
    font-weight: bold;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    margin: 0;
}}

.carousel-overlay p {{
    font-size: 1.2rem;
    margin-top: 10px;
    text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.05);
}}

/* Gradient Fades */
.carousel-wrapper::before,
.carousel-wrapper::after {{
    content: "";
    position: absolute;
    top: 0;
    width: 60px;
    height: 100%;
    z-index: 3;
    pointer-events: none;
}}

.carousel-wrapper::before {{
    left: 0;
    background: linear-gradient(to right, white, transparent);
}}

.carousel-wrapper::after {{
    right: 0;
    background: linear-gradient(to left, white, transparent);
}}

@keyframes scroll {{
    0%   {{ transform: translateX(0); }}
    100% {{ transform: translateX(-50%); }}
}}
</style>

<div class="carousel-wrapper">
    <div class="white-overlay"></div>  <!-- NEW white transparency layer -->
    <div class="carousel-overlay">
        <h1>Helping the European Union for 20 Years.</h1>
        <p>Advocating for families, education, and fairness across Europe.</p>
    </div>
    <div class="carousel-track">
        {img_tags}
        {img_tags}
    </div>
</div>
"""

# Render in Streamlit
html(carousel_html, height=350)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.image("assets/Home/LearnMore_photo.png")

with col2:
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("# Learn more about the people behind this project.")

    if st.button("Learn More", type="primary"):
        st.switch_page('pages/30_About.py')
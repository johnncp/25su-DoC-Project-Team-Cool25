# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st
from datetime import datetime
from io import StringIO
import requests
import json
import logging
import time

# Logger to debug
logger = logging.getLogger(__name__)

# Get current hour
now = datetime.now()
hour = now.hour

# Determine greeting
if hour < 3:
    greeting = "🌚 Working late"
elif 3 <= hour < 12:
    greeting = "🌅 Good morning"
elif 12 <= hour < 16:
    greeting = "☀️ Good afternoon"
elif 16 <= hour < 19:
    greeting = "🌓 Good evening"
else:
    greeting = "🌜 Good night"


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🖼️")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧑‍🧑‍🧒‍🧒")


#### ------------------------ Role of daycare_operator ------------------------
def DaycareHomeNav():
    st.sidebar.page_link(
        "pages/00_Daycare_Home.py", label="Your Home", icon="🛖"
    )


def DaycareEUMemberPredictorNav():
    st.sidebar.page_link(
        "pages/08_Daycare_EU_Member_Predictor.py", label="EU Member Predictor", icon="🇪🇺"
    )


def DaycareResourcesNav():
    st.sidebar.page_link("pages/02_Daycare_Resources.py", label="Resources", icon="📚")

def DaycareBusinessPlanNav():
    st.sidebar.page_link("pages/04_Business_Planner.py", label="Business Planner", icon="💼")


## ------------------------ Role of parent ------------------------
def ParentHomeNav():
    st.sidebar.page_link(
        "pages/10_Parent_Home.py", label="Your Home", icon="🛖"
    )

def ParentEUMemberPredictorNav():
    st.sidebar.page_link("pages/11_Parent_EU_Member_Predictor.py", label="EU Country Predictor", icon="🇪🇺")


def ParentResourcesNav():
    st.sidebar.page_link(
        "pages/17_Parent_Affinity_Resources.py", label="Resources", icon="📚")


def ParentWorkHoursNav():
    st.sidebar.page_link(
        "pages/13_Parent_Work_Hours.py", label="Work Hours Analysis", icon="⏱️"
    )

def ParentDaycareFindNav():
    st.sidebar.page_link("pages/02_Daycare_Resources.py", label="Daycare Finder", icon="🔎")


def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")


def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")

# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st
from datetime import datetime
from io import StringIO
import requests
import json
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Get current hour
now = datetime.now()
hour = now.hour

# Determine greeting
if hour < 3:
    greeting = "🌚 Working late"
elif 3 <= hour < 12:
    greeting = "🌅 Good morning"
elif 12 <= hour < 16:
    greeting = "☀️ Good afternoon"
elif 16 <= hour < 19:
    greeting = "🌓 Good evening"
else:
    greeting = "🌜 Good night"


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🖼️")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧑‍🧑‍🧒‍🧒")


#### ------------------------ Role of daycare_operator ------------------------
def DaycareHomeNav():
    st.sidebar.page_link(
        "pages/00_Daycare_Home.py", label="Your Home", icon="🛖"
    )


def DaycareEUMemberPredictorNav():
    st.sidebar.page_link(
        "pages/08_Daycare_EU_Member_Predictor.py", label="EU Member Predictor", icon="🇪🇺"
    )


def DaycareResourcesNav():
    st.sidebar.page_link("pages/02_Daycare_Resources.py", label="Resources", icon="📚")

def DaycareBusinessPlanNav():
    st.sidebar.page_link("pages/04_Business_Planner.py", label="Business Planner", icon="💼")


## ------------------------ Role of parent ------------------------
def ParentHomeNav():
    st.sidebar.page_link(
        "pages/10_Parent_Home.py", label="Your Home", icon="🛖"
    )

def ParentEUMemberPredictorNav():
    st.sidebar.page_link("pages/11_Parent_EU_Member_Predictor.py", label="EU Country Predictor", icon="🇪🇺")


def ParentResourcesNav():
    st.sidebar.page_link(
        "pages/17_Parent_Affinity_Resources.py", label="Resources", icon="📚")


def ParentWorkHoursNav():
    st.sidebar.page_link(
        "pages/13_Parent_Work_Hours.py", label="Work Hours Analysis", icon="⏱️"
    )

def ParentDaycareFindNav():
    st.sidebar.page_link("pages/02_Daycare_Resources.py", label="Daycare Finder", icon="🔎")


def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")


def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")

def NoteTakingFeature():
    # user_id from session state
    user_id = st.session_state.get("user_id", None)
    
    if not user_id:
        st.sidebar.error("User ID not found. Please log in again.")
        return
    
    # user-specific keys for session state
    user_notes_key = f"notes_{user_id}"
    user_last_updated_key = f"notes_last_updated_{user_id}"
    
    
    if user_notes_key not in st.session_state:
        st.session_state[user_notes_key] = ""
        
    if user_last_updated_key not in st.session_state:
        st.session_state[user_last_updated_key] = None

    

    with st.sidebar.expander("✪ Your Insights", expanded=False):

        # Text area tied to session state
        notes = st.text_area("Pen down your reflections:", 
                           value=st.session_state[user_notes_key], 
                           height=270,
                           key=f"notes_textarea_{user_id}")
        
        
        if not notes.strip():  # Only show if notes are empty
            if st.button("↺ Load Previous Note", use_container_width=True, key=f"load_button_{user_id}"):
                try:
                    response = requests.get(f"http://web-api:4000/notes/notes/{user_id}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, dict) and "note_content" in data and data["note_content"] is not None:
                            st.session_state[user_notes_key] = data["note_content"]
                            st.rerun()  # Refresh to hide the button and show loaded notes
                        else:
                            st.info("No saved notes found")
                            st.session_state[user_notes_key] = ""
                    else:
                        st.error("Failed to load notes")
                except Exception as e:
                    st.error(f"Load error: {str(e)}")
                
                           

        # If notes has changed.
        if notes != st.session_state[user_notes_key]:
            st.session_state[user_notes_key] = notes
            
            # auto-save to API
            try:
                response = requests.post(
                    "http://web-api:4000/notes/notes",
                    json={
                        "user_id": user_id,
                        "note_content": notes
                    }
                )
                if response.status_code == 200:
                    st.success("✓ Notes saved")
                else:
                    st.error("Failed to save notes")
            except Exception as e:
                st.error(f"Save error: {str(e)}")

        st.text("Download as:")

        col1, col2 = st.columns(2)

        with col1:
            # Download Markdown button
            markdown_content = f"# {st.session_state['first_name']}\'s Notes\n\n\n{notes}"
            notes_buffer = StringIO(markdown_content)
            st.download_button(
                label="↓ .md",
                data=notes_buffer.getvalue(),
                use_container_width=True,
                file_name=st.session_state['first_name'] + "s_Notes.md",
                mime="text/markdown"
            )
        
        with col2:
            # Download Plain text button
            notes_buffer = StringIO(notes)
            st.download_button(
                label="↓ .txt",
                data=notes_buffer.getvalue(),
                use_container_width=True,
                file_name=st.session_state['first_name'] + "s_Notes.txt",
                mime="text/plain"
            )
        
        st.caption("Rest assured: \'Your Insights\' are only accessible to you.")
        
def Logout():
    if st.session_state["authenticated"]:
        if st.sidebar.button("❌ Logout", type='secondary'):
            # Save any remaining notes before logout
            user_id = st.session_state.get("user_id", None)
            if user_id:
                user_notes_key = f"notes_{user_id}"
                notes = st.session_state.get(user_notes_key, "").strip()
                if notes:
                    try:
                        requests.post(
                            "http://web-api:4000/notes/notes",
                            json={
                                "user_id": user_id,
                                "note_content": notes
                            }
                        )
                    except:
                        pass  # Silent fail
                
                # Clear user-specific notes from session state only
                if user_notes_key in st.session_state:
                    del st.session_state[user_notes_key]
            
            # Clear authentication session state
            del st.session_state["role"]
            del st.session_state["authenticated"]
            if "user_id" in st.session_state:
                del st.session_state["user_id"]
            if "first_name" in st.session_state:
                del st.session_state["first_name"]
            
            st.switch_page("Home.py")
            


#### ------------------------ Role of politician ------------------------
def PoliticianPageNav():
    st.sidebar.page_link("pages/20_Politician_Home.py", label="Your Home", icon="🖥️")

    st.sidebar.page_link(
        "pages/21_Politician_Birth_Rate_Predictor.py", label="Birth Rate Predictor", icon="🍼"
    )
    st.sidebar.page_link(
        "pages/22_Politician_Legislation_Finder.py", label="Legislation Finder", icon="🔎"
    )
    st.sidebar.page_link("pages/24_Politician_Resources.py", label="Politician Resources", icon="📁")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/eurobebe_logo1.png", width=210)

    st.sidebar.divider()

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        st.sidebar.title(greeting + ", " + st.session_state['first_name'] + "!")

        # Notes Feature
        # YourInsightsWarning() # warning before deleting
        NoteTakingFeature()

        st.sidebar.divider()

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "daycare_operator":
            DaycareHomeNav()
            DaycareEUMemberPredictorNav()
            #DaycareResourcesNav()
            DaycareBusinessPlanNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "parent":
            ParentHomeNav()
            ParentEUMemberPredictorNav()
            ParentDaycareFindNav()
            ParentResourcesNav()
            #ParentWorkHoursNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "politician":
            PoliticianPageNav()
        
        st.sidebar.divider()

def AlwaysShowAtBottom():
    AboutPageNav()
    Logout()
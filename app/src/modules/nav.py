# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st
from datetime import datetime

# Get current hour
now = datetime.now()
hour = now.hour

# Determine greeting
if 5 <= hour < 12:
    greeting = "🌅 Good morning"
elif 12 <= hour < 16:
    greeting = "☀️ Good afternoon"
else:
    greeting = "🌓 Good evening"


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
        "pages/01_Daycare_EU_Member_Predictor.py", label="EU Member Predictor", icon="🇪🇺"
    )


def DaycareResourcesNav():
    st.sidebar.page_link("pages/02_Daycare_Resources.py", label="Resources", icon="📚")


## ------------------------ Role of parent ------------------------
def ParentEUMemberPredictorNav():
    st.sidebar.page_link("pages/11_Parent_EU_Member_Predictor.py", label="EU Member Predictor", icon="🇪🇺")


def ParentResourcesNav():
    st.sidebar.page_link(
        "pages/12_Parent_Resources.py", label="Resources", icon="📚")


def ParentWorkHoursNav():
    st.sidebar.page_link(
        "pages/13_Parent_Work_Hours.py", label="Work Hours Analysis", icon="⏱️"
    )


def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")


def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")


#### ------------------------ Role of politician ------------------------
def PoliticianPageNav():
    st.sidebar.page_link("pages/20_Politician_Home.py", label="Your Home", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_Politician_Birth_Rate_Predictor.py", label="Model", icon="🧮"
    )
    st.sidebar.page_link(
        "pages/22_Politician_Legislation_Finder.py", label="Legislation Finder", icon="🔎"
    )
    st.sidebar.page_link(
        "pages/23_Politician_Family_Time_Resources.py", label="Family Time Resources", icon="🫂"
    )


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

        st.sidebar.divider()

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "daycare_operator":
            DaycareHomeNav()
            DaycareEUMemberPredictorNav()
            DaycareResourcesNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "parent":
            ParentEUMemberPredictorNav()
            ParentResourcesNav()
            ParentWorkHoursNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "politician":
            PoliticianPageNav()
        
        st.sidebar.divider()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("✖️ Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")

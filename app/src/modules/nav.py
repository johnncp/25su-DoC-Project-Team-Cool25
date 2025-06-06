# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st
from datetime import datetime
from io import StringIO

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
        "pages/01_Daycare_EU_Member_Predictor.py", label="EU Member Predictor", icon="🇪🇺"
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
    # Initialize session state on first load
    if "notes" not in st.session_state:
        st.session_state.notes = ""

    with st.sidebar.expander("✪ Your Insights", expanded=False):
        # Text area with value tied to session state
        notes = st.text_area("Pen down your reflections:", value=st.session_state.notes, height=200)

        # Update session state when user types
        st.session_state.notes = notes

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

def YourInsightsWarning():
    # Warning if notes are empty.
    if st.session_state["authenticated"]:
        if st.session_state.get("logout_warning", False):
            container = st.sidebar.container(border=True)
            container.warning("⚠️ \'Your insights\' will be **permanently** deleted upon logout if not downloaded. Are you sure?")

            col1, col2 = container.columns(2)

            with col1:
                if st.button("☆ Cancel", use_container_width=True, type="primary"):
                    st.session_state["logout_warning"] = False
                    st.rerun()

            with col2:
                if st.button("Proceed", use_container_width=True, type="tertiary"):
                    del st.session_state["role"]
                    del st.session_state["authenticated"]
                    del st.session_state["notes"]
                    st.session_state["logout_warning"] = False
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
    #st.sidebar.page_link("pages/23_Politician_Family_Time_Resources.py", label="N/A", icon="⚠️")


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
        YourInsightsWarning() # warning before deleting
        NoteTakingFeature()

        st.sidebar.divider()

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "daycare_operator":
            DaycareHomeNav()
            #DaycareEUMemberPredictorNav()
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

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        notes = st.session_state.get("notes", "").strip()
        if st.sidebar.button("❌ Logout", type='secondary'):
            if notes:
                st.session_state["logout_warning"] = True
            else:
                del st.session_state["role"]
                del st.session_state["authenticated"]
                st.switch_page("Home.py")
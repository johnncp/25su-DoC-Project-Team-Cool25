import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks, AlwaysShowAtBottom

if st.session_state["authenticated"]:
    SideBarLinks()
    AlwaysShowAtBottom()
else:
    SideBarLinks(True)

st.title("About Eurobébé")

st.markdown(
    """
    Is quality of life declining? Are politics uprooting longstanding systems? Do things just feel too unstable? Above all, our project draws these questions to an alarming trend: **declining birth rates** in various nations around the globe. In 2023, the EU saw its [largest decline in birth rate](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250307-1#:~:text=In%202023%2C%203.67%20million%20babies,down%20from%201.46%20in%202022.) since 1961. Exploring this phenomenon deeper, we ask two questions: 

    1. Given rising financial uncertainty, how do weekly working hours correlate with employment rates of parents across different countries in the EU? What nations with more **flexible parental benefits** show higher employment rates for adults with young children (especially mothers)?
    2. Between educational attainment and employment rates, what is the relationship among parents with young children across different EU countries? 

    Our research hopes to combine these complementary analyses to discover what successful policy frameworks that support families to be successful and economically cared for — especially against the diverse European cultural landscapes. Nurturing the project via Eurostat, we hope to reveal insights through data such as gender inequality (wage disparities, labor market participation), work-life balance (commuting burden, conditions of work), social support systems (social safety net, investment in human capital), or safety (crime levels).
    """
)

st.divider()

st.title("About the Authors")

authors = [
    {
        "name": "Sophie Farrell",
        "image": "assets/30_About/sophie_baby_photo.png",
        "bio": "3rd Year Computer Science and Economics Student"
    },
    {
        "name": "Mia Giargiari",
        "image": "assets/30_About/mia_baby_photo.png",
        "bio": "2nd Year Honors Business (Marketing) and Law Student Minoring in Data Science"
    },
    {
        "name": "Emma Kulla",
        "image": "assets/30_About/emma_baby_photo.png",
        "bio": "2nd Year Honors Data Science and Business Administration (Finance) Student"
    },
    {
        "name": "John Nguyen",
        "image": "assets/30_About/john_baby_photo.png",
        "bio": "3rd Year Computer Science and Business Administration (FinTech, Marketing Analytics) Student"
    },
]

# 4-column layout
cols = st.columns(4)

for col, author in zip(cols, authors):
    with col:
        st.image(author["image"], use_container_width=True)
        st.markdown(f"**{author['name']}**")
        st.caption(author["bio"])

st.text("Made with ♡ from Leuven, Belgium. A.D. 2025.")

st.divider()

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")

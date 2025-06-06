import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the title of the page
st.title('Find Daycares')

import streamlit as st
import requests

# User inputs
country = st.text_input("Country Code", "BE")
city = st.text_input("City", "Brussels")
price = st.number_input("Max Monthly Price", min_value=0, value=500)

# Fetch data
if st.button("Search Daycares"):
    params = {
        "country_code": country,
        "city": city,
        "monthly_price": price
    }
    response = requests.get("http://web-api:4000/location/locations")

    if response.status_code == 200:
        data = response.json()
        st.success(f"Found {len(data)} results")
        for item in data:
            st.write(item)
    else:
        st.error("Failed to fetch locations")



# You can access the session state to make a more customized/personalized app experience
#st.write(f"### Hi, {st.session_state['first_name']}.")

# get the countries from the world bank data
#with st.echo(code_location='above'):
    #countries:pd.DataFrame = wb.get_countries()
   
    #st.dataframe(countries)

# the with statment shows the code for this block above it 
#with st.echo(code_location='above'):
    #arr = np.random.normal(1, 1, size=100)
    #test_plot, ax = plt.subplots()
    #ax.hist(arr, bins=20)

    #st.pyplot(test_plot)


#with st.echo(code_location='above'):
    #slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
    #data_crosstab = pd.crosstab(slim_countries['region'], 
                               # slim_countries['incomeLevel'],  
                                #margins = False) 
    #st.table(data_crosstab)

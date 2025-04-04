# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Wuggedi :balloon:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:")

name_on_order = st.text_input('Name on Smoothie:')
st.write('the name will be ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredient_list = st.multiselect('Choose up to 5:', my_dataframe,
                                max_selections=6)
if ingredient_list:
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        if search_on is None:
            search_on = fruit_chosen
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df = st.dataframe(smoothiefroot_response.json(),use_container_width=True)
    st.write(ingredients_string)
    my_instert_stmt = """insert into orders(ingredients,name_on_order)
                        values ('"""+ingredients_string+"""','"""+name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')
    
    st.write(my_instert_stmt)
    if time_to_insert:
        session.sql(my_instert_stmt).collect()
        st.success('Your Smoothie is ordered')
        
    
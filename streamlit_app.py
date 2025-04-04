# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose up to 5:', my_dataframe,
                                max_selections=6)
if ingredient_list:
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    my_instert_stmt = """insert into orders(ingredients,name_on_order)
                        values ('""" + ingredients_string + """
                                ','""" + name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')
    
    st.write(my_instert_stmt)
    if time_to_insert:
        session.sql(my_instert_stmt).collect()
        st.success('Your Smoothie is ordered')
        

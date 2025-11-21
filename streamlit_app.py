# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name of smoothie:")
st.write("The name of the smoothie will be -", name_on_order)

cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    st.write("You selected:", ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''
    for i in ingredients_list:
        ingredients_string += i + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    #st.write(ingredients_string)

    time_to_insert = st.button('Submit Rrder')

    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
        #st.write(my_insert_stmt)
    
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")

# smoothiefroot_reponse = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_reponse)

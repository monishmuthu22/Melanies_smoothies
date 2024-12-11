# Import necessary packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests

# Streamlit app header
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# User input for name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake connection
connection_params = {
    "account": "GYOIACS-MFB56045",
    "user": "MuthuM",
    "password": "Pl@n2workPl@n2work",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "smoothies",
    "schema": "public"
}

try:
    # Create a Snowflake session
    session = Session.builder.configs(connection_params).create()

    # Fetch fruit options and convert to a list
    fruit_options_df = session.table("fruit_options").select(col('FRUIT_NAME')).to_pandas()
    fruit_list = fruit_options_df['FRUIT_NAME'].tolist()

    # Multiselect for ingredients
    ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_list, max_selections=5)
    if ingredients_list:
        ingredients_string = ', '.join(ingredients_list)

        # Insert order into the database
        if st.button('Place Order'):
            try:
                insert_query = f"""
                    INSERT INTO smoothies.public.orders (ingredients, name)
                    VALUES (%s, %s)
                """
                session.sql(insert_query, [ingredients_string, name_on_order]).collect()
                st.success('Your Smoothie is ordered!', icon="✅")
            except Exception as e:
                st.error(f"Error placing order: {e}")
except Exception as conn_error:
    st.error(f"Failed to connect to Snowflake: {conn_error}")
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width = True)

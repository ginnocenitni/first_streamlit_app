import streamlit
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas as pd

path1 = 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt'
my_fruit_list = pd.read_csv(path1)
my_fruit_list = my_fruit_list.set_index("Fruit")

# Let's put a pick list here so they can pick the fruit they want to include
# also, we will use a list to .loc table and exhibit just selected fruits
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index) , ['Avocado' , 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Bring information from FRUITYVICE API using package requests from python

streamlit.header("Fruityvice Fruit Advice!")

#Creating a text box for client choosen fruits. Fruit_choice is a String
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests

#Here I have commented and copy paste the response. We will separete the address into two strings adress + fruit

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

#Here we have used 
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# I have commented the line below instead of deleting it as suggested in the course. 
#streamlit.text(fruityvice_response.json()) #here the data is printed as dictionary (json)

#Let's us make it better to vizualization:

# write your own comment -what does the next line do? - Answere: Normalize json semi-structured data into a table. 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - what does this do? - Answere: Display the table on the page, as did before.  
streamlit.dataframe(fruityvice_normalized)

# Query Our Trial Account Metadata (snowflake.connector)
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

# Query Some Data, Instead
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT* from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Let's put a pick list here so they can ADD the fruit they want to include
add_my_fruit = streamlit.multiselect("Add some fruits:", list(my_fruit_list.index))
streamlit.write('Thanks for adding:', add_my_fruit)



import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas as pd

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

#New fruit selection scheme with try if and so on... 
## Making function

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
        streamlit.error("Please, select a fruit to get information")
   else:
        back_from_function = get_fruityvice_data(fruit_choice) 
        streamlit.dataframe(back_from_function)
                         
except URLError as e:
    streamlit.error()
         
#stoping the code run here to debug
#streamlit.stop()

#import snowflake.connector

# Query Our Trial Account Metadata (snowflake.connector)
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

# Query Some Data, Instead
streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT* from fruit_load_list")
         return my_cur.fetchall()
 
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
         return "Thanks for adding:" + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
if streamlit.button('Add Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)

streamlit.stop()

# Let's put a pick list here so they can ADD the fruit they want to include
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
streamlit.write('Thanks for adding:', add_my_fruit)

#This will not work correctly but let's go with it now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")




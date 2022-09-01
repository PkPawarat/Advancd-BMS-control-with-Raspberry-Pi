import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title = 'HVAC control')
st.header('Data feedback')
st.subheader('Test')
### --- Load DATAFRAME
#df = pd.read_excel(io= 'log_static_previous_team.xlsx',
 #                   engine='openpyxl',
  #                  sheet_name = 'log_static',
   #                 header= 0,
    #                nrows=1527,
     #               usecols='B:E')
                    
##df["hour"] = pd.to_datetime(df["Time"],format= "%H:%M:%S")
#temp =st.number_input('Insert temperature',min_value=10.00,max_value=30.00,step=0.5)
#st.write('The set temp',temp)
#st.dataframe(df)
#fig = px.line(df.set_index('Time'))
#st.plotly_chart(fig)
df_input_test = pd.read_excel('input_test.xlsx')
st.write(df_input_test)
st.sidebar.header("Input Time and Temp")
temp_form = st.sidebar.form('temp_form')
time_input = temp_form.time_input('Time_input')
temp_input = temp_form.number_input('Temperature input',min_value = 18.00, max_value = 30.00, value= 23.00,step = 0.5)
add_data = temp_form.form_submit_button()
#if add_data:
 #   new_data = {'time': time_input, ''}

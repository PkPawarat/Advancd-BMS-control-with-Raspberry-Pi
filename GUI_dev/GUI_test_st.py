
from distutils.command.sdist import sdist
from posixpath import supports_unicode_filenames
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title = 'HVAC control',
                   page_icon=':chart_with_upwards_trend:',
                   layout = 'wide',
                   initial_sidebar_state='expanded')
st.title('HVAC control and feedback')
st.markdown('##')
st.subheader('Data input ')
### --- input new data set with form


df_input_test = pd.read_excel(io ='input_test.xlsx',
                              engine = 'openpyxl',
                              sheet_name='Sheet1',
                              header= 0,
                              usecols='A:C')
     
st.sidebar.header("Input Time ,Temperature and Humidity")
   
input_form = st.sidebar.form('input_form')
time_input = input_form.time_input('Time input')
temp_input = input_form.number_input('Temperature input',min_value = 18.00, max_value = 30.00, value= 23.00,step = 0.5)
humid_input = input_form.number_input('Humidity input',min_value = 30.00,max_value = 70.00,value = 50.00,step = 5.00)
add_data = input_form.form_submit_button()
if add_data:
     new_data_input = {'Time' : time_input,'Temp':temp_input,'Humid':humid_input}
     df_input_test = df_input_test.append(new_data_input,ignore_index = True)
     
df_input_test.to_excel("input_test.xlsx",index = False)
st.sidebar.header(" AC simple control")    
## AC STATE BUTTON
ac_state = st.sidebar.radio (" Set AC state",('OFF','ON '))
if ac_state =='OFF':
     st.sidebar.write('AC IS OFF')
else:
     st.sidebar.write('AC is ON')
## FAN SPEED BUTTON     
fan_speed = st.sidebar.radio("Set Fan speed",('LOW','MEDIUM','HIGH'))
if fan_speed =='LOW':
     st.sidebar.write('FAN SPEED IS LOW')
if fan_speed =='MEDIUM':
     st.sidebar.write('FAN SPEED IS MEDIUM')
if fan_speed =='HIGH':
     st.sidebar.write('FAN SPEED IS HIGH')
## SUPPLY FAN BUTTON
supply_fan = st.sidebar.radio("Set supply fan mode",('STANDARD','CONTINOUS'))
if supply_fan == 'STANDARD':
     st.sidebar.write(' SUPPLY FAN MODE IS STANDARD')
if supply_fan == 'CONTINOUS':
     st.sidebar.write('SUUPLY FAN MODE IS CONTINUOS')
## AC MODE BUTTON
ac_mode = st.sidebar.radio("Set AC mode",('HEAT ONLY','COOL ONLY','AUTO CHANGE OVER','FAN ONLY'))
if ac_mode == 'HEAT ONLY':
     st.sidebar.write('AC MODE IS HEAT ONLY')
if ac_mode == 'COOL ONLY':
     st.sidebar.write('AC MODE IS COOL ONLY')
if ac_mode == 'AUTO CHANGE OVER':
     st.sidebar.write('AC MODE IS AUTO CHANGE OVER')
if ac_mode == 'FAN ONLY':
     st.sidebar.write('AC MODE IS FAN ONLY')
fig_input_temp = px.line(df_input_test,x='Time',y='Temp',width = 600, height = 400,title = f'<b>  Input Temperature Diagram<b>')    
fig_input_humid = px.line(df_input_test,x = 'Time', y = 'Humid',width= 600,height = 400,title = f'<b> Input Humid Diagram<b>')
st.write(df_input_test)
## sorting input data according to time


## ---- Temperature feedback data
st.subheader('Input and Feedback diagram')
df_feedback_temp = pd.read_excel(io= 'log_static_previous_team.xlsx',
                    engine='openpyxl',
                    sheet_name = 'log_static',
                    header= 0,
                    nrows=1527,
                    usecols='B:E')
                    
#df["hour"] = pd.to_datetime(df["Time"],format= "%H:%M:%S")
#st.dataframe(df_feedback_temp)
fig_feedback_temp = px.line(df_feedback_temp.set_index('Time'),width =600,height = 400, title =f'<b> Feedback Temperature Diagram<b>')
## ---display input and feedback chart side by side
temp_left_column, temp_right_column = st.columns(2)
temp_left_column.plotly_chart(fig_input_temp, use_container_width = True)
temp_right_column.plotly_chart(fig_feedback_temp, use_container_width = True)
st.plotly_chart(fig_input_humid)
print(df_input_test)
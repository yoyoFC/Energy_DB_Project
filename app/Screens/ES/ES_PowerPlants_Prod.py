import streamlit as st
import pandas as pd
import numpy as np
import psycopg2, psycopg2.extras
import sys 
import os
import plotly.express as px

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

###################################
#Database connection 

query = 'Select "Year_Num","Sys_Annual_AVG_Prod_Cost_cent_kWh" from public."EO_Production_Cost"'
df_Annual_AVG = gt_func.Execute_query(query)
df_Annual_AVG.rename(columns={0: 'Year',1:'Avg_Cent_kWh'}, inplace=True)

df_fuel = gt_func.Reload_fuel(2007)
year_selected = 2007
df_plants = gt_func.Reload_Plants('ALL')
fuel_type = 'ALL'
####################################
#Streamlit screen layout

st.title('Power Plants and Production Cost')

st.subheader('Austin Energy oversees a diverse mix of more than 5,000 MW of total generation capacity and operates three natural gas powered plants in the Austin area. The next chart will explain how the kwh production cost has been changed from 2006 to 2019. Additionally, we will analyze the fuel cost by year. How expensive is produce a kW in Austin?')


########################################
#Main sections
col1,col2 = st.columns(2)

with col1:
    st.info("Annual average production cost (cent/kWh)")
    fig = px.bar(df_Annual_AVG, x='Year', y='Avg_Cent_kWh',
             hover_data=['Avg_Cent_kWh', 'Year'], color='Avg_Cent_kWh',
             labels={'pop':'Average cost by cent/kWh'}, height=400)
    st.plotly_chart(fig)
    
with col2:
    st.info("Data reference display on the chart")
    st.table(df_Annual_AVG)

#####################################
#Second section 

with st.form(key='refresh_data1'):
    col3,col4 = st.columns(2)
    with col3:
        fuel_type = st.selectbox('Plants available based on fuel type:',('ALL', 'Coal', 'Nuclear','Gas'))
        
        
    with col4:
        year_selected = st.slider('Select the Year to refresh cost based on Fuel type:',min_value=2007, max_value=2019, step=1)
    submit_button = st.form_submit_button(label='Refresh')  
    if submit_button:
        df_plants, df_fuel = gt_func.Reload_charts(fuel_type,year_selected)
    
st.markdown('#')

###################################
#Third section 
plant,fuel = st.columns(2)

with plant:
    st.warning("Power plants analysis")
    st.dataframe(df_plants)
with fuel:
    st.warning("Fuel type distribution")
    #st.dataframe(df_fuel)
    fig = px.pie(df_fuel, names= df_fuel['Fuel_Type'], values= df_fuel['Fuel_Cost'])
    fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
        ))
    st.plotly_chart(fig)
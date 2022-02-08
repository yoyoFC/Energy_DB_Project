import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import requests
import plotly.graph_objects as go

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

dir_sys = os.path.join(os.getcwd(), "app", "docs")
sys.path.insert(0, dir_sys)
import config

#########################################################
#Database connection, calling the function Execute_query
#Input: query
#output: dataframe
query = 'Select * from public."G_Charging_Stations"' 
df = gt_func.Execute_query(query)

query = ('Select Distinct("Postal_Code")::text as ZipCode from public."G_Charging_Stations" '+
        'order by ZipCode DESC')
df_zip = gt_func.Execute_query(query)

query = ('select ' + "'ALL' as Category " +
        'Union '+
        'Select Distinct("Category") as Category from public."G_Charging_Stations" '+
        'order by Category ASC')
df_category = gt_func.Execute_query(query)
         
         
query = ('select ' + "'ALL' as Category " +
        'Union ' +
        'Select Distinct("City") as Category from public."G_Charging_Stations" '+
        'order by Category ASC')
df_city = gt_func.Execute_query(query)
         
#####################################
#Rename columns of df
df.rename(columns={0: 'Property Name',1:'Address',2:'nan',3:'City',4:'State',5:'Zip_Code',6:'Number of Ports',7:'Pricing Policy',8:'Usage Access',9:'Category',10:'Sub Category',11:'Port 1',12:'Port 2',13:'Latitude',14:'Longitude',15:'Voltage',16:'Amps' }, inplace=True)


#########################################
#Streamlit layout - graphic
st.title("Electric charging stations available in Austin")

with st.form(key='refresh_data'):
    
    location,category = st.columns(2)

    with location:
        city_selected = st.selectbox("Filter the charging locations based on city:",df_city[0])
        zip_selected = []
        #zip_selected = st.multiselect('Select zip (empty selection will display all zip codes available)',df_zip[0])
    
    with category:
        category_selected = st.radio("Select the main filter of for the data",df_category[0])
        
    submit_button = st.form_submit_button(label='Submit') 

if submit_button:
    if len(zip_selected) == 0:
        zip_selected = 'ALL'
    df = gt_func.Reload_Map(df,city_selected,zip_selected,category_selected)
    
st.markdown('#')

col1,col2 = st.columns(2)
with col1:
    ##################################################################################
    #Displayu the chart based on the previous filter selection
    fig = go.Figure(go.Scattermapbox(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=df['Address'],
        ))

    fig.update_layout(
        hovermode='closest',
        margin=dict(t=0,b=0,l=0, r=0),
        width=750, height=700,
        mapbox=dict(
            accesstoken=st.secrets["mapbox_access_token"],
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=30.33,
                lon=-97.75
            ),
            pitch=0,
            zoom=10
        )
    )

    st.plotly_chart(fig)

with col2:
    st.dataframe(df[['Address','City','Category','Number of Ports']])

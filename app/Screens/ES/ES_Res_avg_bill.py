import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly_express as px
import plotly.graph_objects as go

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

##############################################################################
#database connection - default values
query = ('Select ' +
'TO_CHAR( ' + 
    'TO_DATE (Extract(Month from public."EO_Residential_Avg_Bill"."Date")::text, '+ " 'MM' " +'),' + " 'Mon' " + 
    ') AS "month_name", ' + 
'Extract(Year from public."EO_Residential_Avg_Bill"."Date") as year_Num,' + 
' "Average_kWH", "Fuel_Charge_cents_kWH", "Average_Bill","Month_num" ' +
' from public."EO_Residential_Avg_Bill"' + 
' ORDER BY "year_num","month_name" ASC' )

df = gt_func.Execute_query(query)

df.rename(columns={0: 'Month',1:'Year',2:'Average_kWH',3:'Fuel_Charge_Cents_kWH',4:'Average Bill',5:'Month_ID'}, inplace=True)

convert_dict = {'Year': int}

df=df.astype(convert_dict)

df_1, df_2 = gt_func.Reload_Avg_Bill(df,2007,2007)
Year_1 = 2007
Year_2 = 2007
df_1 = df_1.sort_values('Month_ID')
df_2 = df_2.sort_values('Month_ID')

############################################################################################
#Streamlit layout

st.title("Residential Average Bill - data")


st.subheader('Residential customers use an average of about 1,000 kWh of electricity per month, with usage higher during hot summer months and lower in the winter. View tables show monthly average usage in kWh by month for residential customers starting in 2000. Tables include monthly fuel charges and electric bill amounts.')

##########################################
#Section 1 filters - form
with st.form(key='refresh_data'):
    col1,col2 = st.columns(2)

    with col1:
        Year_1 = st.slider('Select the first year:',min_value=2007, max_value=2019, step=1)
        
    with col2:
        Year_2 = st.slider('Select the second year:',min_value=2007, max_value=2019, step=1)
    submit_button = st.form_submit_button(label='Refresh')  
    if submit_button:
        df_1, df_2 = gt_func.Reload_Avg_Bill(df,Year_1,Year_2)
        df_1 = df_1.sort_values('Month_ID')
        df_2 = df_2.sort_values('Month_ID')

########################################
#Section 2 Main plot
fig = go.Figure()
vName_1 = "Avg. Bill " + str(Year_1)
vName_2 = "Avg. Bill " + str(Year_2)
# Add traces
fig.add_trace(
    go.Scatter(x=df_1['Month'], y=df_1['Average Bill'], name=vName_1)
)

fig.add_trace(
    go.Scatter(x=df_2['Month'], y=df_2['Average Bill'], name=vName_2)
)

y_text = "<b>Average Bill </b> (USD)"
fig.update_yaxes(title_text=y_text)

fig.update_layout(
    showlegend = True,
    width = 1500,
    height = 600
)
# Set x-axis title
fig.update_xaxes(title_text="Year(" + str(Year_1) + " vs " + str(Year_2) + ")")
st.plotly_chart(fig)        
        
col3,col4 = st.columns(2)

with col3:
    st.info('Year 1 selected:' + str(Year_1))
    st.dataframe(df_1[['Year','Month','Month_ID','Average_kWH','Average Bill']])
with col4:
    st.info('Year 2 selected:' + str(Year_2))
    st.dataframe(df_2[['Year','Month','Month_ID','Average_kWH','Average Bill']])

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.graph_objects as go
import plotly.express as px
import time
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from plotly.subplots import make_subplots

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

##################################################################################
#Load data in front before start dsplaying objects

#Project square query + dataframe result.
y_text = ""
vSQL = ('Select t3."Fiscal_Year", t3."Single_Family" as "Single_Family",' +
	   't4."Project_sq" as Multifamily, t3."Commercial" as "Commercial" ' +
       'from('+
       'Select t1."Fiscal_Year", t1."Project_sq" as "Single_Family",' + 
       't2."Project_sq" as "Commercial" ' +
       'from '
       '(Select "Class","Fiscal_Year","Project_sq" ' +  
       'from public."G_Building_Project_Agg" '+
       'where "Class" = ' + "'Single Family')t1 " +
       'inner join ' +
       '(Select "Class","Fiscal_Year","Project_sq" '+ 
       'from public."G_Building_Project_Agg" ' +
       'where "Class" = ' + "'Commercial')t2 " +
       'on t1."Fiscal_Year" = t2."Fiscal_Year" '+
       ') as t3 ' +
       'inner join '+
       '(Select "Class","Fiscal_Year","Project_sq" '+ 
       'from public."G_Building_Project_Agg" ' +
       'where "Class" = ' + "'Multifamily')t4 " +
       'on t3."Fiscal_Year" = t4."Fiscal_Year" ' +
       'order by t3."Fiscal_Year" ASC')

df_sq = gt_func.Execute_query(vSQL)
df_sq.set_index(0)
df_sq.rename(columns={0: 'Year',1:'Single Family',2:'Multifamily',3:'Commercial'}, inplace=True)

#Demand saving query + dataframe result.
vSQL = ('Select t3."Fiscal_Year", t3."Single_Family" as "Single_Family",' +
	   't4."Demand_Savings_KW" as Multifamily, t3."Commercial" as "Commercial" ' +
       'from('+
       'Select t1."Fiscal_Year", t1."Demand_Savings_KW" as "Single_Family",' + 
       't2."Demand_Savings_KW" as "Commercial" ' +
       'from '
       '(Select "Class","Fiscal_Year","Demand_Savings_KW" ' +  
       'from public."G_Building_Project_Agg" '+
       'where "Class" = ' + "'Single Family')t1 " +
       'inner join ' +
       '(Select "Class","Fiscal_Year","Demand_Savings_KW" '+ 
       'from public."G_Building_Project_Agg" ' +
       'where "Class" = ' + "'Commercial')t2 " +
       'on t1."Fiscal_Year" = t2."Fiscal_Year" '+
       ') as t3 ' +
       'inner join '+
       '(Select "Class","Fiscal_Year","Demand_Savings_KW" '+ 
       'from public."G_Building_Project_Agg" ' +
       'where "Class" = ' + "'Multifamily')t4 " +
       'on t3."Fiscal_Year" = t4."Fiscal_Year" ' +
       'order by t3."Fiscal_Year" ASC')


df_demand = gt_func.Execute_query(vSQL)
df_demand.set_index(0)
df_demand.rename(columns={0: 'Year',1:'Single Family',2:'Multifamily',3:'Commercial'}, inplace=True)

#Electric saving query + dataframe result.
vSQL = ('Select t3."Fiscal_Year", t3."Single_Family" as "Single_Family",' +
	   't4."Electric_Savings_MWH" as Multifamily, t3."Commercial" as "Commercial" ' +
       'from('+
       'Select t1."Fiscal_Year", t1."Electric_Savings_MWH" as "Single_Family",' + 
       't2."Electric_Savings_MWH" as "Commercial" ' +
       'from '
       '(Select "Class","Fiscal_Year","Electric_Savings_MWH" ' +  
       'from public."G_Building_Project_Agg" '+
       'where "Class" = ' + "'Single Family')t1 " +
       'inner join ' +
       '(Select "Class","Fiscal_Year","Electric_Savings_MWH" '+ 
       'from public."G_Building_Project_Agg" ' +
       'where "Class" = ' + "'Commercial')t2 " +
       'on t1."Fiscal_Year" = t2."Fiscal_Year" '+
       ') as t3 ' +
       'inner join '+
       '(Select "Class","Fiscal_Year","Electric_Savings_MWH" '+ 
       'from public."G_Building_Project_Agg" ' +
       'where "Class" = ' + "'Multifamily')t4 " +
       'on t3."Fiscal_Year" = t4."Fiscal_Year" ' +
       'order by t3."Fiscal_Year" ASC')

df_saving = gt_func.Execute_query(vSQL)
df_saving.set_index(0)
df_saving.rename(columns={0: 'Year',1:'Single Family',2:'Multifamily',3:'Commercial'}, inplace=True)

###############################################################
#Function to update the dataframe based on selection.
def Reload_Chart(filter_option):
    if filter_option == 'Project square feet over the years':
        df = df_sq
        
    if filter_option == 'Demand by customer type':
        df = df_demand
        
    if filter_option == 'Electricity savings data by customer type':
        df = df_saving
    return df

###############################################################
#Default values to upload screen
filter_option = 'Project square feet over the years'
df = Reload_Chart(filter_option)

##############################################################
#Screen layout and objects

st.title("Green Development in Austin")

st.subheader("The comparison in green energy use between multifamily, single family, and commercial structures")

###########################################################
#MAIN PLOT with 3 selectors (forms)
with st.form(key='refresh_data'):
    filter_option = st.radio("Select the different graphics available:",['Project square feet over the years','Demand by customer type','Electricity savings data by customer type'])
    submit_button = st.form_submit_button(label='Submit') 
    
if submit_button:
    df = Reload_Chart(filter_option)

fig_1 = go.Figure()
# Add traces
df.sort_values(["Year"]).reset_index(drop=True)
fig_1.add_trace(
    go.Scatter(x=df['Year'], y=df['Single Family'], name="Single Family")
)

fig_1.add_trace(
    go.Scatter(x=df['Year'], y=df['Multifamily'], name="Multifamily")
)

fig_1.add_trace(
    go.Scatter(x=df['Year'], y=df['Commercial'], name="Commercial")
)

# Set y-axes titles
if filter_option == 'Project square feet over the years':
    y_text = "<b>Project dimension </b> (sq2)"
        
if filter_option == 'Demand by customer type':
    y_text = "<b>Demand savings </b> (KW)"
        
if filter_option == 'Electricity savings data by customer type':
    y_text = "<b>Elec. Savings </b> (MW)"
fig_1.update_yaxes(title_text=y_text)

fig_1.update_layout(
    showlegend = True,
    width = 1500,
    height = 600
)
# Set x-axis title
fig_1.update_xaxes(title_text="Year(2007 - 2020)")
st.plotly_chart(fig_1)

######################################################
#Section 2: indivisual displayer ->Expanders

with st.expander("Single Family"):
    st.write("""
         This section display the data for the Single Family green building development.
     """)
    query = ('SELECT public."G_Building_Project_Agg"."Class", public."G_Building_Project_Agg"."Fiscal_Year",' +                         'public."G_Building_Project_Agg"."Project_sq", public."G_Building_Project_Agg"."Electric_Savings_MWH"' +
            'FROM public."G_Building_Project_Agg" where public."G_Building_Project_Agg"."Class" =' + "'Single Family'")
    
    
    df = gt_func.Execute_query(query)
    
    lottie_img_SF = gt_func.load_lottieurl(Animations.GD_SF)
    col1,col2 = st.columns(2)
    with col1:
        st_lottie(lottie_img_SF, key="img1")
    with col2:
        st.dataframe(df)

with st.expander("Multi Family"):
    st.write("""
         This section display the data for the Multi Family green building development.
     """)
    query = ('SELECT public."G_Building_Project_Agg"."Class", public."G_Building_Project_Agg"."Fiscal_Year",' +                         'public."G_Building_Project_Agg"."Project_sq", public."G_Building_Project_Agg"."Energy_Savings_MBTU",'+                     'public."G_Building_Project_Agg"."Electric_Savings_MWH", public."G_Building_Project_Agg"."Gas_Saving"' +
            'FROM public."G_Building_Project_Agg" where public."G_Building_Project_Agg"."Class" =' + "'Multifamily'")
    
    df = gt_func.Execute_query(query)
    
    df.rename(columns={0: 'Category',1:'Fiscal Year',2:'Project Square Footage',3:'Energy Savings',4:'Electric Savings',5:'Gas Savings'}, inplace=True)
    lottie_img_MF = gt_func.load_lottieurl(Animations.GD_MF)
    col3,col4 = st.columns(2)
    with col3:
        st_lottie(lottie_img_MF, key="img2")
    with col4:
        st.dataframe(df)
    
    
with st.expander("Commercial"):
    st.write("""
         This section display the data for the Commercial green building development.
     """)
    query = ('SELECT public."G_Building_Project_Agg"."Class", public."G_Building_Project_Agg"."Fiscal_Year",'+                         'public."G_Building_Project_Agg"."Project_sq", public."G_Building_Project_Agg"."Energy_Savings_MBTU",'+                     'public."G_Building_Project_Agg"."Electric_Savings_MWH", public."G_Building_Project_Agg"."Gas_Saving"' +
            'FROM public."G_Building_Project_Agg" where public."G_Building_Project_Agg"."Class" =' + "'Commercial'")
    
    df = gt_func.Execute_query(query)
    
    df.rename(columns={0: 'Category',1:'Fiscal Year',2:'Project Square Footage',3:'Energy Savings',4:'Electric Savings',5:'Gas Savings'}, inplace=True)

    lottie_img_CO = gt_func.load_lottieurl(Animations.GD_CO)
    col5,col6 = st.columns(2)
    with col5:
        st_lottie(lottie_img_CO, key="img3")
    with col6:
        st.dataframe(df)
    

    
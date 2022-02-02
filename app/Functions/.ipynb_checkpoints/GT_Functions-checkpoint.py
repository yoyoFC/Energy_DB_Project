import pandas as pd
import numpy as np
import os
import sys
import streamlit as st
import time
import requests
import requests
import psycopg2, psycopg2.extras

dir_sys = os.path.join(os.getcwd(), "app", "docs")
sys.path.insert(0, dir_sys)
import config

@st.cache
########################################################################
#Function: This function verify the animation exsit and still available.

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

########################################################################
#Function: This function perfomr scrapping instruction to bring data from ERCOT
#return a dictionary with multiple values

def scrapping_ERCOT():
    vSQL = 'select * from public."EO_Ercot" order by "TS_Epoch" desc limit 1'
    
    df = Execute_query(vSQL)
    
    # Parse the HTML
    vStatus = str(df.iloc[0][0])

    #Numeric values
    vReserve = df.iloc[0][1].replace("MW", "")
    
    #status    
    vCurrentDemand = df.iloc[0][2].replace("MW", "")
    vCommitCapacity = df.iloc[0][3].replace("MW", "")
    
    #description
    vLastUpdate = str(df.iloc[0][4])
    vCurrentDesc = 'The amount of power the Texas grid is currently serving'
    vCommitCapacityDesc = 'The amount of power the Texas grid has available'
    
    #RETURN
    return {'status':vStatus,
            'reserve':vReserve,
            'current':vCurrentDemand,
            'capacity':vCommitCapacity,
            'updated':vLastUpdate,
            'current_desc':vCurrentDesc,
            'commit_desc':vCommitCapacityDesc}

################################################################################
#Function: This function stablish a database connection and execute a query.
#return a dataframe
def Execute_query(vQuery):
    connection = psycopg2.connect(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASS,                                        database=config.DB_NAME)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(vQuery)
    result = cursor.fetchall()  
    df = pd.DataFrame(result)
    connection.close()
    return df

################################################################################
#Functions : Reload the widget selection and calls other function (Execute query)
def Reload_Widgets(vYear,vFilter):
    
    if vFilter == 'Producer Type':
        vSQL = ('Select public."G_Emmision_US"."Producer_Type", public."G_Emmision_US"."CO2_Tons" as CO2,' +
                'public."G_Emmision_US"."SO2_Tons" as SO, public."G_Emmision_US"."NOx_Tons" as NOx from public."G_Emmision_US" WHERE ' + 
                ' public."G_Emmision_US"."Year" = ' + str(vYear) + ' and public."G_Emmision_US"."State" = ' + "'TX' AND " +
                ' public."G_Emmision_US"."Producer_Type" <> ' + "'Total Electric Power Industry' and " + 
                ' public."G_Emmision_US"."Energy_Source" = ' + " 'All Sources' order by " +
                ' public."G_Emmision_US"."Year",public."G_Emmision_US"."Producer_Type" ASC')
    else:
        #Energy Source
        vSQL = ('Select public."G_Emmision_US"."Energy_Source", public."G_Emmision_US"."CO2_Tons" as CO2,' +
                ' public."G_Emmision_US"."SO2_Tons" as SO, public."G_Emmision_US"."NOx_Tons" as NOx from public."G_Emmision_US" WHERE ' + 
                ' public."G_Emmision_US"."Year" = ' + str(vYear) + ' and public."G_Emmision_US"."State" = '+ "'TX' AND " +
                ' public."G_Emmision_US"."Producer_Type" = ' + " 'Total Electric Power Industry'and " + 
                ' public."G_Emmision_US"."Energy_Source" <> ' + "'All Sources' order by " +
                ' public."G_Emmision_US"."Year",public."G_Emmision_US"."Energy_Source" ASC ')
    
    df_raw = Execute_query(vSQL)
    
    if vFilter == 'Producer Type':
        df_raw.rename(columns={0: 'Producer Type',1:'CO2',2:'SO2',3:'NOX'}, inplace=True)
    else:
        df_raw.rename(columns={0: 'Energy Source',1:'CO2',2:'SO2',3:'NOX'}, inplace=True)
    
    return df_raw


################################################################################
#Functions : Reload the map widget based on previous selection
def Reload_Map(df,city_selected,zip_selected,category_selected):
    if city_selected == 'ALL':
        df = df[df['City'].notnull()]
    else:
        df = df[df['City']==city_selected]
        
    if zip_selected == 'ALL':
        df = df[df['Zip_Code'].notnull()]
    else:
        df = df.query('Zip_Code in @zip_selected')
        #df = df[df['Zip Code'].isin(zip_selected)]
    
    if category_selected == 'ALL':
         df = df[df['Category'].notnull()]
    else:
        df = df[df['Category']==category_selected]

    return df

################################################################################
#Functions : Execute query to filter plants based on fuel type
def Reload_Plants(fuel_type):

    if fuel_type == 'ALL':
        vSQL = 'Select "Power_Plant","Year_installed","Fuel" from public."EO_Power_Plants"'
    else:
        vSQL = ('Select "Power_Plant","Year_installed","Fuel" from public."EO_Power_Plants" where "Fuel" = ' +
                "'" + fuel_type + "'" )
        
    df_raw = Execute_query(vSQL)
    df_raw.rename(columns={0: 'Power Plant',1:'Year installed',2:'Fuel'}, inplace=True)
    
    return df_raw
    
################################################################################
#Functions : Execute query to filter fuel type distribution based on year
def Reload_fuel(year_selected):
    vSQL = ('Select * from public."EO_PowerSupply_Cost" where ' + 
           '("Fuel_Type" = ' + "'Gas' OR " + '"Fuel_Type" = ' + "'Coal' OR " +
           '"Fuel_Type" = ' + "'Nuclear') AND " + '"Year_Num" = ' + str(year_selected) + 'order by "Fuel_Type" ASC')
    df_raw = Execute_query(vSQL)
    df_raw.rename(columns={0: 'Fuel_Type',1:'Fuel_Cost',2:'Fuel_Cost_Per',3:'Year_Num'}, inplace=True)
    
    return df_raw

###############################################################################
#Function this function work with the form , calls two functions and return two dataframe
def Reload_charts(fuel_type,year_selected):
    df_plants = Reload_Plants(fuel_type)
    df_fuel = Reload_fuel(year_selected)
    
    return df_plants, df_fuel

###############################################################################
def Reload_Avg_Bill(df,Year_1,Year_2):
    df_1 = df.loc[df['Year'] == Year_1]
    df_2 = df.loc[df['Year'] == Year_2]
    
    return df_1,df_2
                    
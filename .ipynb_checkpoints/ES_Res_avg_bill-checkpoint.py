import streamlit as st
import pandas as pd
import numpy as np
import psycopg2 as db_connect

host_name = "dataviz.cgq2ewzuuqs1.us-east-2.rds.amazonaws.com"
db_user = "postgres"
db_password = "ElPeruano_2021"
db_name = "postgres"
db_port = 5432
connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=db_port)

cursor = connection.cursor()

##query = 'SELECT * FROM public.' + '"EO_Customer_Class" '
query = ('Select ' +
'TO_CHAR( ' + 
    'TO_DATE (Extract(Month from public."EO_Residential_Avg_Bill"."Date")::text, '+ " 'MM' " +'),' + " 'Mon' " + 
    ') AS "month_name", ' + 
'Extract(Year from public."EO_Residential_Avg_Bill"."Date") as year_Num,' + 
' "Average_kWH", "Fuel_Charge_cents_kWH", "Average_Bill" ' +
' from public."EO_Residential_Avg_Bill"' + 
' ORDER BY "month_name","year_num" ' )

cursor.execute(query)
data = cursor.fetchall()
connection.close()

df = pd.DataFrame(data)

df.rename(columns={0: 'Month',1:'Year',2:'Average_kWH',3:'Fuel_Charge_Cents_kWH',4:'Average Bill'}, inplace=True)

convert_dict = {'Year': int}

df=df.astype(convert_dict)

st.title("Residential Averga Bill - data")

st.dataframe(df)
import streamlit as st
import pandas as pd
import numpy as np
import psycopg2, psycopg2.extras
import config
import plotly.graph_objects as go
import plotly.express as px
import time
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

lottie_SF = "https://assets10.lottiefiles.com/private_files/lf30_dvqxua.json"
lottie_MF = "https://assets10.lottiefiles.com/packages/lf20_thq99fhd.json"
lottie_CO = "https://assets10.lottiefiles.com/private_files/lf30_ljfP8c.json"
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


connection = psycopg2.connect(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASS, database=config.DB_NAME)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
pattern = "Single Family"
st.title("Green Development in Austin")

#st.header("is a header needed?")

st.subheader("The comparison in green energy use between multifamily, single family, and commercial structures")

st.write("info info info")

line_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['single family', 'multifamily', 'commercial'])
st.line_chart(line_data)

with st.expander("Single Family"):
    st.write("""
         This section display the data for the Single Family green building development.
     """)
    query = ('SELECT public."G_Building_Project_Agg"."Class", public."G_Building_Project_Agg"."Fiscal_Year",' +                         'public."G_Building_Project_Agg"."Project_sq", public."G_Building_Project_Agg"."Elecitrc_Savings_MWH"' +
            'FROM public."G_Building_Project_Agg" where public."G_Building_Project_Agg"."Class" =' + "'Single Family'")
    cursor.execute(query)
    result = cursor.fetchall()
    
    df = pd.DataFrame(result)
    lottie_img_SF = load_lottieurl(lottie_SF)
    col1,col2 = st.columns(2)
    with col1:
        st_lottie(lottie_img_SF, key="img1")
    with col2:
        st.dataframe(df)

with st.expander("Multi Family"):
    st.write("""
         This section display the data for the Multi Family green building development.
     """)
    query = ('SELECT public."G_Building_Project_Agg"."Class", public."G_Building_Project_Agg"."Fiscal_Year",' +                         'public."G_Building_Project_Agg"."Project_sq", public."G_Building_Project_Agg"."Energy_Savings_MBTU",'+                     'public."G_Building_Project_Agg"."Elecitrc_Savings_MWH", public."G_Building_Project_Agg"."Gas_Saving"' +
            'FROM public."G_Building_Project_Agg" where public."G_Building_Project_Agg"."Class" =' + "'Multifamily'")
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    df.rename(columns={0: 'Category',1:'Fiscal Year',2:'Project Square Footage',3:'Energy Savings',4:'Electric Savings',5:'Gas Savings'}, inplace=True)
    lottie_img_MF = load_lottieurl(lottie_MF)
    col3,col4 = st.columns(2)
    with col3:
        st_lottie(lottie_img_MF, key="img2")
    with col4:
        st.dataframe(df)
    
    
with st.expander("Commercial"):
    st.write("""
         This section display the data for the Commercial green building development.
     """)
    query = ('SELECT public."G_Building_Project_Agg"."Class", public."G_Building_Project_Agg"."Fiscal_Year",'+                         'public."G_Building_Project_Agg"."Project_sq", public."G_Building_Project_Agg"."Energy_Savings_MBTU",'+                     'public."G_Building_Project_Agg"."Elecitrc_Savings_MWH", public."G_Building_Project_Agg"."Gas_Saving"' +
            'FROM public."G_Building_Project_Agg" where public."G_Building_Project_Agg"."Class" =' + "'Commercial'")
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    df.rename(columns={0: 'Category',1:'Fiscal Year',2:'Project Square Footage',3:'Energy Savings',4:'Electric Savings',5:'Gas Savings'}, inplace=True)

    lottie_img_CO = load_lottieurl(lottie_CO)
    col5,col6 = st.columns(2)
    with col5:
        st_lottie(lottie_img_CO, key="img3")
    with col6:
        st.dataframe(df)
    connection.close()

    
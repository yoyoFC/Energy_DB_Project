import streamlit as st
import pandas as pd
import numpy as np

#st.title('ENERGY GREEN DEVELOPMENT')
st.markdown("<h1 style='text-align: center; color: green; font-size: 100px'>ENERGY GREEN DEVELOPMENT</h1>", unsafe_allow_html=True)

pages = {
        "Overview":'GD_Home.py',
        "Single Family building": 'GD_Single_Family.py',
        "Multifamily building":'GD_Multifamily.py',
        "Commercial building": 'GD_Commercial.py',
        "Green Building project": 'GD_Green_Building_Project.py',
        "Electrical Vehicles charging stations": 'GD_Electric_Vehicles_Stations.py',
        "Emmisions": 'GD_Emmisions.py'
    }

pages_list = list(pages)
option = st.sidebar.radio("Select the additional views for Green Development:",pages_list)
#st.text(option)

fname_to_run = pages[option]
#if option != "Overview":
with open(fname_to_run, encoding="utf8") as f:
    filebody = f.read()
    exec(filebody,globals())
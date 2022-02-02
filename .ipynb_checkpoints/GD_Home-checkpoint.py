import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

measure1 = time.time()
measure2 = time.time()
url = "https://www.youtube.com/watch?v=nesNYAcjw-g"
lottie_main = "https://assets8.lottiefiles.com/packages/lf20_rbdxztbu.json"
lottie_main_2 = "https://assets4.lottiefiles.com/private_files/lf30_psn7xxju.json"
lottie_wind = "https://assets8.lottiefiles.com/private_files/lf30_yi91simh.json"
lottie_solar = "https://assets2.lottiefiles.com/packages/lf20_lf6sg88x.json"
lottie_selected = lottie_main

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

col1, col2 = st.columns([1, 3])
with col1:
    lottie_img_solar = load_lottieurl(lottie_solar)
    st_lottie(lottie_img_solar, key="img1")

with col2:  
    st.header(" - Emmision in Texas from 1990 to 2019")
    st.header(" - This is othe tex")
    

col3,col4 = st.columns([3, 1])
with col3:
    st.video(url)
with col4:
    lottie_img_main = load_lottieurl(lottie_main)
    st_lottie(lottie_img_main, key="img2")
    lottie_img_main_2 = load_lottieurl(lottie_main_2)
    st_lottie(lottie_img_main_2, key="img22")

    
col5, col6 = st.columns([1, 3])
with col5:
    lottie_img_wind = load_lottieurl(lottie_wind)
    st_lottie(lottie_img_wind, key="img3")

with col6:
    st.header(" - Text ")
    st.header(" - More text")
    
    

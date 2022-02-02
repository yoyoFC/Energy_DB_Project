import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import os
import sys

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

col1, col2 = st.columns([1, 3])
with col1:
    lottie_img_solar = gt_func.load_lottieurl(Animations.GD_solar)
    st_lottie(lottie_img_solar, key="img1")

with col2:  
    st.header(" - Austin Energy offer incentives for Solar solutions.")
    st.header(" - As a residential customer you can: Earn solar credits that apply to your electric bill and increase the property value of your home.")
    st.header(" - As a commercial customer, you can: Reduce your demand charges and Earn Leadership in Energy and Environmental Design (LEED) certification points.")
    link='For information about solar rates and other details check out this [link](https://austinenergy.com/ae/green-power/solar-solutions/value-of-solar-rate)'
    st.markdown(link,unsafe_allow_html=True)

col3,col4 = st.columns([3, 1])
with col3:
    st.video(Animations.GD_video)
with col4:
    lottie_img_main = gt_func.load_lottieurl(Animations.GD_main)
    st_lottie(lottie_img_main, key="img2")
    lottie_img_main_2 = gt_func.load_lottieurl(Animations.GD_main_2)
    st_lottie(lottie_img_main_2, key="img22")

    
col5, col6 = st.columns([1, 3])
with col5:
    lottie_img_wind = gt_func.load_lottieurl(Animations.GD_wind)
    st_lottie(lottie_img_wind, key="img3")

with col6:
    st.header(" - The GreenChoice customer program (Texas wind energy) are making a big imacpt in the community. ")
    st.header(" - The program removed carbon emmision equal to 109,634 cars")
    st.header(" - Greenhouse gas emissions avoided by installing 319,278,251 LED bulbs instead of incandescent")
    st.header(" - Powering nearly 86,000 homes for a year with wind energy instead of fossil fuels")
    link2='For information about Green Choices Business Offerings check out this [link](https://austinenergy.com/ae/green-power/greenchoice/business-offerings)'
    st.markdown(link2,unsafe_allow_html=True)
    
    
    
    

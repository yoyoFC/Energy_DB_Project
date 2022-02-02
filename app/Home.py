import streamlit as st
from PIL import Image
import os
import sys
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

dir_test = ""
dir_test = os.path.join(os.getcwd(), "app")
dir_sys = os.path.join(os.getcwd(), "app", "Resources", "Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

ImageWelcome = os.path.join(os.getcwd(), "app", "Resources", "Images","Austin_Back_carlos-alfonso.jpg")
Logo = Animations.scientist

introduction_1 = "After the devastating winter freeze last year, Texas energy use & distribution was put under a microscope. Texas produces and consumes more electricity than any other state; in fact, it's the only state that runs a stand-alone independent electricity grid. Therefore, Texans demanded to know why the power grid suddenly failed us in such a dire time & what is being done to prevent future tragedies.\n "

introduction_2 = "\n To determine what can be changed regarding our energy structure, we've compiled some data sets from the City of Austin. While analyzing this subset of the Texas power grid, we're hoping to answer: what is the current consumer demand & has it increased over the last few years? What energy sources are we using? What are green alternatives in the capital and how are those being developed and/or utilized?"


background = Image.open(ImageWelcome)

with st.container():
    st.markdown("<h1 style='text-align: center; color: green; font-size: 100px'>Energy Summary Dashboard Austin(Texas)</h1>", unsafe_allow_html=True)
    st.image(background, caption="foto provided by https://unsplash.com/@csfoto", width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")

  
st.subheader(introduction_1)
st.subheader(introduction_2)
st.markdown("<h1 style='text-align: left; color: green;'>The Green Team</h1>", unsafe_allow_html=True)
st.text("Jun 2021 - Feb 2022")
Logo_img = gt_func.load_lottieurl(Logo)
st_lottie(Logo_img, key="img")
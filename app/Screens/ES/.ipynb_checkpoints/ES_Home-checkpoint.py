import streamlit as st
import pandas as pd
import numpy as np
import os as os
import sys as sys
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func


ERCOT = gt_func.scrapping_ERCOT()
        
ColStatus,Re,Res_Desc,De,De_Desc,Cap,Cap_Desc = st.columns(7)

with ColStatus:
    st.success("Grid Status")
    text = '<p style="font-family:Courier; color:Green; font-size: 28px;">{vStatus}</p>'
    text = f"""
            <style>
            p.a {{
              font: bold 14px Verdana;
              color: green;
            }}
            </style>
            <p class="a">{ERCOT.get('status')}</p>
            """
    st.markdown(text, unsafe_allow_html=True)

with Re:
    st.success("Operating Reserves")
    st.metric(label="Mega Watts", value = ERCOT.get('reserve').strip())

with Res_Desc:
    st.success("Update")
    st.write(ERCOT.get('updated'))

with De:
    st.error("Current Demand")
    st.metric(label="Mega Watts", value = ERCOT.get('current'))

with De_Desc:
    st.error("Desc:")
    st.write(ERCOT.get('current_desc'))

with Cap:
    st.info("Commit Capacity")
    st.metric(label="Mega Watts", value = ERCOT.get('capacity'))

with Cap_Desc:
    st.info("Desc:")
    st.write(ERCOT.get('commit_desc'))

col1, col2 = st.columns([3,1])

with col1:
    st.video(Animations.ES_video)

with col2:
    lottie_img = gt_func.load_lottieurl(Animations.ES_light_statistic)
    st_lottie(lottie_img, key="img1")
    
    lottie_img_2 = gt_func.load_lottieurl(Animations.ES_lightball)
    st_lottie(lottie_img_2, key="img2")

#browser.windows[0].close()
    


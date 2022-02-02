import streamlit as st
import pandas as pd
import numpy as np
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_img = "https://assets10.lottiefiles.com/private_files/lf30_lhnmhnbn.json" 
lottie_img_2 = "https://assets4.lottiefiles.com/packages/lf20_o1p93l2m.json"
url_video = "https://www.youtube.com/watch?v=9yKRz08buaA"
vStatus = ""

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://www.ercot.com//' 
browser.visit(url)
    
# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')

#Numeric values
tag_box = html_soup.find_all('div', class_='condition')
counter = 0 
for tag in tag_box:
    counter += 1
    if counter == 1:
        vReserve = tag.text
    if counter == 2:
        vCurrentDemand = tag.text
    if counter == 3:
        vCommitCapacity = tag.text

#status    
tag_box = html_soup.find_all('div', class_='status')
for tag in tag_box:
    word = tag.text
    vStatus = vStatus + " " + word

#description
tag_box = html_soup.find_all('div', class_='desc')
counter = 0
for tag in tag_box:
    counter += 1
    if counter == 1:
        vLastUpdate = tag.text
    if counter == 2:
        vCurrentDesc = tag.text
    if counter == 3:
        vCommitCapacityDesc = tag.text


      
        
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
            <p class="a">{vStatus}</p>
            """
    st.markdown(text, unsafe_allow_html=True)
    #st.write("STATUS: " + vStatus)

with Re:
    st.success("Current Demand")
    st.metric(label="Mega Watts", value = vReserve)

with Res_Desc:
    st.success("Update")
    st.write(vLastUpdate)

with De:
    st.error("Current Demand")
    st.metric(label="Mega Watts", value = vCurrentDemand)

with De_Desc:
    st.error("Desc:")
    st.write(vCurrentDesc)

with Cap:
    st.info("Commit Capacity")
    st.metric(label="Mega Watts", value = vCommitCapacity)

with Cap_Desc:
    st.info("Desc:")
    st.write(vCommitCapacityDesc)


col1, col2 = st.columns([3,1])

with col1:
    st.video(url_video)

with col2:
    lottie_img = load_lottieurl(lottie_img)
    st_lottie(lottie_img, key="img1")
    
    lottie_img_2 = load_lottieurl(lottie_img_2)
    st_lottie(lottie_img_2, key="img2")

browser.windows[0].close()
    


import streamlit as st
import os
import sys

def main():
    
    ## Set page configuration
    st.set_page_config(page_title="ENERGY DASHBOARD - Austin Texas", initial_sidebar_state="expanded", layout="wide")
    
    ## Main pages sections
    sections = {
        "Home": os.path.join(os.getcwd(), "app", "Home.py"),
        "ENERGY SUMMARY": os.path.join(os.getcwd(), "app", "energy_summary.py"),
        "GREEN DEVELOPMENT": os.path.join(os.getcwd(), "app", "green_development.py"),
    }
    
    ## Pass the main pages selection as list and put it on a select box
    apps = list(sections)
    key = st.sidebar.selectbox('Select an section',apps)
    st.sidebar.markdown('#')
    
    ## based on the selection open the file (screen name)
    fname_to_run = sections[key]
    with open(fname_to_run, encoding="utf8") as f:
        filebody = f.read()
    exec(filebody,globals())
                  
if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import numpy as np

st.title('Power Plants and Production Cost')

st.subheader('Dataset sample')

df = pd.DataFrame(
    np.random.randn(10,2),
    columns=['x','y'])
st.line_chart(df)
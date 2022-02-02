import streamlit as st
import pandas as pd
import numpy as np
import psycopg2 as db_connect
import os
import sys
import plotly.express as px
import plotly.graph_objs as go

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

query = 'SELECT * FROM public.' + '"EO_Customer_Class" '
df = gt_func.Execute_query(query)

df.rename(columns={0: 'Year',1:'Residential',2:'Commercial',3:'Industrial',4:'Other', 5:'Total'}, inplace=True)

st.title("Customer Class data")
st.header(" Austin Energy has four main customer classes: residential, commercial, industrial and other. The next views will show how the number of each of these groups increased since 2007.")

col1,col2,col3,col4 = st.columns(4)
with col1:
    st.info('Residential Customers')
    st.write(
        """    Live in single-family dwellings, mobile homes, townhouses, or individually metered apartment units. """)
    
with col2:
    st.info('Commercial Customers')
    st.write(
        """    Small to large businesses that fall under Austin Energy’s secondary level of service. This means Austin Energy owns, operates, and maintains the equipment (wires, transformers, etc.) supplying power to those facilities". """)

with col3:
    st.info('Industrial')
    st.write(
        """   (Primary) customers take service at high voltage (12,500 volts or higher) and own, operate and maintain their own equipment. Consequently, Austin Energy experiences lower overall system losses and it costs less to serve these customers. """)

with col4:
    st.info('Other')
    st.write(
        """   The final class, other, typically refers to street lighting and facilities such as ballparks. """)

st.table(df)


fig = go.Figure()
# Add traces
#df.sort_values(["Year"]).reset_index(drop=True)
fig.add_trace(
    go.Scatter(x=df['Year'], y=df['Residential'], mode='markers',
              marker=dict(size=df["Residential"]/10000), name = "Residential")
)

fig.add_trace(
    go.Scatter(x=df['Year'], y=df['Commercial'],mode='markers',
              marker=dict(size=df["Commercial"]/1000),name="Commercial")
)

fig.add_trace(
    go.Scatter(x=df['Year'], y=df['Industrial'],mode='markers',
              marker=dict(color='#8c564b',size=df["Industrial"]/10),name="Industrial")
)

fig.add_trace(
    go.Scatter(x=df['Year'], y=df['Other'],mode='markers',
              marker=dict(size=df["Other"]/100), name = "Other")
)

# Set y-axes titles
y_text = "<b>Total Customers </b>"
fig.update_yaxes(title_text=y_text)

fig.update_layout(
    showlegend = True,
    width = 1500,
    height = 600
)

# Set x-axis title
fig.update_xaxes(title_text="Year(2007 - 2020)")
st.plotly_chart(fig)


st.header(" -The total number of customer has been increased in all the different classes which increased the demand and forced ERCOT to increase the kWh production.")
st.header(" -The class with the most significant growth is residential, this is the class with the most significant growth is residential, this responds to the increase in new residents in Texas, especially in Austin.")


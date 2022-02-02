import streamlit as st
import pandas as pd
import numpy as np
import psycopg2 as db_connect
import os
import sys
from PIL import Image
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


dir_sys = os.path.join(os.getcwd(), "app", "Resources","Animations")
sys.path.insert(0, dir_sys)
import Animations

dir_sys = os.path.join(os.getcwd(), "app", "Resources","Functions")
sys.path.insert(0, dir_sys)
import GT_Functions as gt_func

#############################################
#Define images file path address
imageCO = os.path.join(os.getcwd(), "app", "Resources","Images","CO2.png")
imageSO = os.path.join(os.getcwd(), "app", "Resources","Images","SO2.png")
imageNO = os.path.join(os.getcwd(), "app", "Resources","Images","NOX.png")

##############################################
#Loading by default
df = gt_func.Reload_Widgets(1990,'Producer Type')


################################################
#SECTION 1
st.title("Emmision in Texas from 1990 to 2019")

vSQL_1 = ('Select public."G_Emmision_US"."Year", Sum(public."G_Emmision_US"."CO2_Tons") as CO2,' +
        'Sum(public."G_Emmision_US"."SO2_Tons") as SO,' +
        'Sum(public."G_Emmision_US"."NOx_Tons") as NOx from ' +          
        'public."G_Emmision_US" WHERE ' +
        'public."G_Emmision_US"."State" =' + " 'TX' AND " +
        'public."G_Emmision_US"."Energy_Source" =' + "'All Sources' and " +
        'public."G_Emmision_US"."Producer_Type" = ' + " 'Total Electric Power Industry' " +
        'group by public."G_Emmision_US"."State", public."G_Emmision_US"."Year" ' +
        'order by "G_Emmision_US"."Year" ASC')

df_1 = gt_func.Execute_query(vSQL_1)
df_1.set_index(0)
df_1.rename(columns={0: 'Year',1:'CO',2:'SO',3:'NO'}, inplace=True)

fig_1 = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig_1.add_trace(
    go.Scatter(x=df_1['Year'], y=df_1['CO'], name="CO data"),
    secondary_y=False,
)

fig_1.add_trace(
    go.Scatter(x=df_1['Year'], y=df_1['SO'], name="SO data"),
    secondary_y=True,
)

fig_1.add_trace(
    go.Scatter(x=df_1['Year'], y=df_1['NO'], name="NO data"),
    secondary_y=True,
)

# Set y-axes titles
fig_1.update_yaxes(title_text="<b>CO</b> (Metric Tons)", secondary_y=False)
fig_1.update_yaxes(title_text="<b>SO / NO</b> (Metric Tons)", secondary_y=True)

fig_1.update_layout(
    showlegend = True,
    width = 1500,
    height = 600
)
# Set x-axis title
fig_1.update_xaxes(title_text="Year(1990 - 20219)")
st.plotly_chart(fig_1)

#################################################################    
#Section 2
st.title("Summary by Year")

st.markdown('#')

with st.form(key='refresh_data'):
    
    YearChart_sel,filter_Type = st.columns(2)

    types = {'Producer':['Electric Utility','IPP NAICS-22 Non-Cogen', 'IPP NAICS-22 Cogen',
                         'Commercial Non-Cogen', 'Commercial Cogen', 'Industrial Non-Cogen',
                         'Industrial Cogen'],
             'Source':['Coal', 'Natural Gas', 'Petroleum', 'Wood and Wood Derived Fuels', 'Other Biomas',
                       'Other Gases']}

    with YearChart_sel:
        #year_selected = st.number_input('Year:', min_value=1990, max_value=2019, step=1)
        year_selected = st.slider('Select the Year to refresh the charts',min_value=1990, max_value=2019, step=1)
        chart_selected = st.selectbox('Select a chart type to display the data',('Pie Chart','Bargraph','Table'))
    
    with filter_Type:
        filter_option = st.radio("Select the main filter of for the data",['Producer Type','Energy Source'])
        
    submit_button = st.form_submit_button(label='Submit') 

if submit_button:
    df = gt_func.Reload_Widgets(year_selected,filter_option)
    
st.markdown('#')

######################################################################################
#Section 3 : Sections for each gas
#CO section
col1,col2,col3 = st.columns(3)
with col1:
    st.info('CARBON DIOXIDE')
    icon1 = Image.open(imageCO)   
    st.image(icon1)
    
with col2:
    st.info('Description')
    st.write(
        """    
    - Chemical formula: CO2 (carbon atom covalently double bonded to two oxygen atoms)
    - Oher names: Carbonic acid gas, Carbonic anhydride, Carbonic dioxide and Carbon (IV) oxide.  
    - Since Industrial revolution, it have increased the concentration in the atmosphere causing global warning. 
    - It is used by the food, oil and chemical industry. It has a varied commerical uses, one of the most popular is the sparkle in carbonaded beverages.
    - It is an asphyxiant gas but not classified as toxic in low concentration.
    - In concentration up to 1% (10,000 ppm) it will make some people feel drowsy and give the lungs a stuffy feeling. 
    - Concentration of 7% to 10%, may cause suffocation, headaches, visual,hearing dysfunction and unconscioness within a few minutes to an hour. 
        """)
    
with col3: 
    st.info('Chart Section')
    if chart_selected == 'Table': 
        df_table = pd.DataFrame(df.iloc[: , 0:2])
        st.dataframe(df_table)
    if chart_selected == 'Pie Chart': 
        fig = px.pie(df, names= df[filter_option], values= df['CO2'])
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
        ))
        st.plotly_chart(fig)
    if chart_selected == 'Bargraph':
        fig = px.bar(df, x= df['CO2'], y= df[filter_option], width = 600, height=500,orientation = 'h')
        st.plotly_chart(fig)

######
#SO section
col4,col5,col6 = st.columns(3)
with col4:
    st.error('SULFUR DIOXIDE')
    icon1 = Image.open(imageSO)   
    st.image(icon1)
    
with col5:
    st.error('Description')
    st.write(
        """    
    - Chemical formula: SO2 
    - Other names: Sulfuruous anhydride and Sulfur(IV) oxide. 
    - Toxic gas, it can be released by volcanic activity, copper extraction and the burning of fossil fuels (coal, oiul and diesel) by power plants and other industrial facilities. 
    - Short tearm exposures to SO2 can harm the human respiratory system and make breathing difficult. People with asthma are sensitive to these effects. 
    -Exposure to high doses can cause pulmonary edema, bronchial inflammation, and laryngeal spasm and edema with possible airway obstruction.There is no antidote for sulfur dioxide.
    - At high concetrations, can harm trees and plants by damage foiliage and decreasing growth.
    - SO2 and other sulfur oxides can contribute to acid ran which can hamr sensitive ecosystems.
    - Like nitrogen dioxide, sulfur dioxide can create secondary pollutants once released into the air.
        """
    )
    
with col6: 
    st.error('Chart Section')
    if chart_selected == 'Table':
        df_table = pd.DataFrame(df[filter_option])
        df_table = df_table.join(df['SO2'])
        st.dataframe(df_table)
    if chart_selected == 'Pie Chart': 
        fig = px.pie(df, names= df[filter_option], values= df['SO2'])
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
        ))
        st.plotly_chart(fig)
    if chart_selected == 'Bargraph':
        fig = px.bar(df, x= df['SO2'], y= df[filter_option], width = 600, height=500,orientation = 'h')
        st.plotly_chart(fig)
######
#SO section
col7,col8,col9 = st.columns(3)
with col7:
    st.success('NITRIC OXIDE')
    icon1 = Image.open(imageNO)   
    st.image(icon1)
    
with col8:
    st.success('Description')
    st.write(
        """    
    - Chemical formula: NOx. It is shorthand for molecules containing one nitrogen and one or more oxygen atom.
    - NOx is a generic term for the nitrogen oxides that are most relevant for air pollution: NO / NO2.
    - It is considered a family of poisonous, highly reactive gases. These gases are released when fuel is burned at high temperatures. 
    - NOx are emitted by automobiles, trucks arious non-road vehicles (e.g., construction equipment, boats, etc.) as well as industrial sources such as power plants, industrial boilers, cement kilns, and turbines.
    - When NO x  and volatile organic compounds (VOCs) react in the presence of sunlight, they form photochemical smog, a significant form of air pollution. The presence of photochemical smog increases during the summer when the incident solar radiation is higher.
    - Children, people with lung diseases such as asthma, and people who work or exercise outside are particularly susceptible to adverse effects of smog such as damage to lung tissue and reduction in lung function.
    - It has also been associated with heart disease, diabetes, birth outcomes, and all-cause mortality, but these nonrespiratory effects are less well-established.
        """
    )
    
with col9: 
    st.success('Chart Section')
    if chart_selected == 'Table':
        df_table = pd.DataFrame(df[filter_option])
        df_table = df_table.join(df['NOX'])
        st.dataframe(df_table)
        
    if chart_selected == 'Pie Chart': 
        fig = px.pie(df, names= df[filter_option], values= df['NOX'])
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
        ))
        st.plotly_chart(fig)
    if chart_selected == 'Bargraph':
        
        #fig_3 = go.Figure(go.Bar(x= df['NOX'], y= df[filter_option],orientation = 'h')
        fig = px.bar(df, x= df['NOX'], y= df[filter_option], width = 600, height=500,orientation = 'h')
        st.plotly_chart(fig)
        
        
st.header(" - ERCOT has been working strongly in decrease the emission in Texas, the result in the last 19 year shows a reduction of 76% in NO and 75% and SO (the most toxic gases for the environment.")
st.header(" - The CO emmision increased in in 1.8%. Something to keep in mind is the increment of coal as energy source between 1990 and 2019.")
st.header(" -The US energy information administation has released the carbon emissions for 2020, and it decreased in 11% in compare with 2019.The 2020 decline in U.S. energy-related CO2 emissions was historic.")
st.header(" -The COGEN energy producer (utilization of the normally wasted heat energy produced by a power plant)had increased in the last 19 year, this contribute to the reduce of emmission and the growth of the power plants capacity.")
        

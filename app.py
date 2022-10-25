import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

@st.cache(ttl=60*5, max_entries=20)
def load_data():
    data=pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
    return data
data=load_data()


st.write("""
# Covid19 Tracking App 🚑

[Coronavirus COVID19 API](https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest#81447902-b68a-4e79-9df9-1b371905e9fa) is used to get the data in this app.
""")

img = Image.open("Coronavirus.jpg")
st.image(img)

st.write('*Coronavirus is officially a pandemic. Since the first case in december the disease has spread fast reaching almost every corner of the world.'+
         'They said it\'s not a severe disease but the number of people that needs hospital care is growing as fast as the new cases.'+
         'Some governments are taking measures to prevent a sanitary collapse to be able to take care of all these people.'+
         'I\'m tackling this challenge here. Let\'s see how some countries/regions are doing!*')

st.sidebar.subheader("""Created with 💖 in India by [Sreeja Biswas](https://github.com/SreejaBiswas) from """)
st.sidebar.image('images.png', width = 250)

st.sidebar.write("***Animated clip for awareness:-***")
video_file = open('video.mp4', 'rb')
video_bytes = video_file.read()
st.sidebar.video(video_bytes)

st.sidebar.title('Select the parameters to analyze Covid-19 situation')

select = st.sidebar.selectbox('Select a State',data['State'])
#get the state selected in the selectbox
state_data = data[data['State'] == select]
select_status = st.sidebar.radio("Covid-19 patient's status", ('Confirmed',
'Active', 'Recovered', 'Deceased'))

def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
    'Status':['Confirmed', 'Active', 'Recovered', 'Deaths'],
    'Number of cases':(dataset.iloc[0]['Confirmed'],
    dataset.iloc[0]['Active'], dataset.iloc[0]['Recovered'],
    dataset.iloc[0]['Deaths'])})
    return total_dataframe
state_total = get_total_dataframe(state_data)

st.sidebar.title("Click on the checkbox to visualize the bar chart")
if st.sidebar.checkbox("Show Analysis by State", True, key=1):
    st.markdown("## **State level analysis**")
    st.markdown("### Overall Confirmed, Active, Recovered and " +
    "Deceased cases in %s yet" % (select))
    if not st.checkbox('Hide Graph', False, key=2):
        state_total_graph = px.bar(
        state_total, 
        x='Status',
        y='Number of cases',
        labels={'Number of cases':'Number of cases in %s' % (select)},
        color='Status')
        st.plotly_chart(state_total_graph)

st.sidebar.write("Conclusion")
st.sidebar.write("*The coronavirus disease continues to spread across the world following a trajectory that is difficult to predict. The health, humanitarian and socio-economic policies adopted by countries will determine the speed and strength of the recovery.*")

def get_table():
    datatable = data[['State', 'Confirmed', 'Active', 'Recovered', 'Deaths']].sort_values(by=['Confirmed'], ascending=False)
    datatable = datatable[datatable['State'] != 'State Unassigned']
    return datatable
datatable = get_table()

img = Image.open("virus.jpg")
st.image(img)

st.markdown("### Covid-19 cases in India")
st.markdown("The following table gives you a real-time analysis of the confirmed, active, recovered and deceased cases of Covid-19 pertaining to each state in India.")
st.dataframe(datatable) # will display the dataframe
st.table(datatable)# will display the table
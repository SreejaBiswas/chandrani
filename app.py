import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache(ttl=60*5, max_entries=20)
def load_data():
    data=pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
    return data

data=load_data()

st.markdown('<style>description{color: blue;}</style>',unsafe_allow_html=True)
st.title('Covid-19 in India')
st.markdown("<description>The objective of this website is to offer an on-going assessment of COVID-19's impact in India.</description>",unsafe_allow_html=True)
st.sidebar.title('Select the parameters to analyze Covid-19 situation')
st.sidebar.checkbox("Show Analysis by State", True, key=1)
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
if st.sidebar.checkbox("Show Analysis by State", True, key=2):
    st.markdown("## **State level analysis**")
    st.markdown("### Overall Confirmed, Active, Recovered and " +
    "Deceased cases in %s yet" % (select))
    if not st.checkbox('Hide Graph', False, key=3):
        state_total_graph = px.bar(
        state_total, 
        x='Status',
        y='Number of cases',
        labels={'Number of cases':'Number of cases in %s' % (select)},
        color='Status')
        st.plotly_chart(state_total_graph)

def get_table():
    datatable = data[['State', 'Confirmed', 'Active', 'Recovered', 'Deaths']].sort_values(by=['Confirmed'], ascending=False)
    datatable = datatable[datatable['State'] != 'State Unassigned']
    return datatable
datatable = get_table()
st.markdown("### Covid-19 cases in India")
st.markdown("The following table gives you a real-time analysis of the confirmed, active, recovered and deceased cases of Covid-19 pertaining to each state in India.")
st.dataframe(datatable) # will display the dataframe
st.table(datatable)# will display the table
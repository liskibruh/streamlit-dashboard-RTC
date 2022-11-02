import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

#APP_TITLE='Liverpool- RTC Report'
#APP_SUB_TITLE='Source: xyz'

def display_accidents_count(df, year, severity_status, accident_severity, metric_title):
    df=df[(df['Year']== year)]
    if severity_status:
        df=df[df['Accident_Severity']==severity_status]
        df.drop_duplicates(inplace=True)
        total=df[accident_severity].count()
        st.metric(metric_title,'{:,}'.format(total))

def display_casualties_count(df, year, severity_status, no_of_casualties, metric_title):
    df=df[(df['Year']== year)]
    if severity_status:
        df=df[df['Accident_Severity']==severity_status]
        df.drop_duplicates(inplace=True)
        total=df[no_of_casualties].sum()
        st.metric(metric_title,'{:,}'.format(total))

def display_map(df,year):
    df=df[df['Year']==year]
    map=folium.Map(location=[51.477928, -0.001545],zoom_start=6,scrollWheelZoom=False)
    st_map=st_folium(map, width=700, height=450)

def main():
    APP_TITLE='Liverpool RTC Report'
    st.title(APP_TITLE)

    ## DATA
df=pd.read_csv('accident_data_complete1.csv')
year=2006
severity_status=2
#accident_severity='Accident_Severity'  
#metric_title=f'# of {severity_status} Accidents'
st.subheader(f'{year} Road Accidents Facts')
col1,col2=st.columns(2)
with col1:
    display_accidents_count(df, year, severity_status, 'Accident_Severity', f'# of {severity_status} Accidents')
with col2:    
    display_casualties_count(df, year, severity_status, 'Number_of_Casualties', f'# of {severity_status} Accidents Casualties')


display_map(df,year)


st.write(df.sample(20))
#st.write(df.shape)
st.write(df.columns)


if __name__ == "__main__":
    main()
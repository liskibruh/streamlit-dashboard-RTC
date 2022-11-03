import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu

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
    map=folium.Map(location=[51.509865, -0.118092],zoom_start=6,scrollWheelZoom=False)#, tiles='CartoDB positron')
    
  #  choropleth=folium.Choropleth(
   #     geo_data='world-administrative-boundaries.geojson',
    #    data=df,
    #    columns=([['Latitude', 'Longitude']],'Number_of_Casualties')
    #)
    #choropleth.geojson.add_to(map)
    
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

with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=['Accidents','Visualizations', 'About']
    )

if selected=='Accidents':
    year_list=list(df['Year'].unique())
    year_list.sort()
    year=st.sidebar.selectbox('Year',year_list,len(year_list)-1)
    severity_status=st.sidebar.radio('Severity Status', [1,2])
    #st.write(year_list)
    st.header(f'{year} Accidents of {severity_status} Severity')
    st.subheader('Road Accidents Facts')
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
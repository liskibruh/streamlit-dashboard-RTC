import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from PIL import Image

#APP_TITLE='Liverpool- RTC Report'
#APP_SUB_TITLE='Source: xyz'

def display_accidents_count(df, year, severity_status, accident_severity, metric_title):
    df=df[(df['Year_y']== year)]
    if severity_status:
        df=df[df['Accident_Severity']==severity_status]
        df.drop_duplicates(inplace=True)
        total=df[accident_severity].count()
        st.metric(metric_title,'{:,}'.format(total))

def display_casualties_count(df, year, severity_status, no_of_casualties, metric_title):
    df=df[(df['Year_y']== year)]
    if severity_status:
        df=df[df['Accident_Severity']==severity_status]
        df.drop_duplicates(inplace=True)
        total=df[no_of_casualties].sum()
        st.metric(metric_title,'{:,}'.format(total))

def display_map(df,year,severity_status):
    df=df[df['Year_y']==year]
    #map=folium.Map(location=[51.509865, -0.118092],zoom_start=20,scrollWheelZoom=False)#, tiles='CartoDB positron')
    if severity_status:
        df=df[df['Accident_Severity']==severity_status]
  #  choropleth=folium.Choropleth(
   #     geo_data='world-administrative-boundaries.geojson',
    #    data=df,
    #    columns=([['Latitude', 'Longitude']],'Number_of_Casualties')
    #)
    #choropleth.geojson.add_to(map)
    
    #st_map=st_folium(map, width=700, height=450)
        dfmap=df[["Latitude","Longitude"]]
        dfmap= dfmap.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
    #st.write(dfmap)
    st.map(dfmap,zoom=5)

def main():
    st.set_page_config(page_title='Omdena Liverpool', layout='wide')
    #st.set_page_config(layout='wide')
    st.markdown(
    """
    <style>
    .block-container.css-18e3th9.egzxvld2 {
    padding-top: 0;
    }
    header.css-vg37xl.e8zbici2 {
    background: none;
    }
    .css-tw2vp1.e1tzin5v0 {
    gap: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    APP_TITLE='Predicting RTC severity using Machine Learning'
    col1, col2 = st.columns((1, 3))
    with col1:
        st.image("https://github.com/liskibruh/streamlit-dashboard-RTC/blob/main/assets/omdenaliverpoollogo.png?raw=true")
    with col2:
        st.image("https://raw.githubusercontent.com/liskibruh/streamlit-dashboard-RTC/main/assets/accidents1104x271.png")
    # st.title(APP_TITLE)
    st.markdown("<h1 style='text-align: center; color: #3a469d;'>Predicting RTC severity using Machine Learning</h1>", unsafe_allow_html=True)
    st.write('Over the last few years improvements to roads in the UK have been implemented across the country in order to create a safer roading system with some great effect.  \nThe number of **road traffic collisions** are reported to be in decline.  \nUsing datasets from the Department of Transport, we hope to be able to uncover the probability of the severity of a collision.')
    ## DATA
    df=pd.read_csv('data/full_accident_dataset.csv')
    year=2006
    severity_status='Serious'
    #accident_severity='Accident_Severity'  
    #metric_title=f'# of {severity_status} Accidents'

    with st.sidebar:
        selected=option_menu(
            menu_title="Main Menu",
            options=['Accidents','Visualizations', 'About']
        )

    if selected=='Accidents':
        year_list=list(df['Year_y'].unique())
        year_list.sort()
        year=st.sidebar.selectbox('Year_x',year_list,len(year_list)-1)
        severity_status=st.sidebar.radio('Severity Status', ['Slight','Serious','Fatal'])
        #st.write(year_list)
        #st.subheader(f'Year: {year}') 
        #st.subheader(f'Severity Status: {severity_status}')
        #st.subheader('Road Accidents Facts')
        col1,col2,col3,col4=st.columns(4)
        with col1:
            display_accidents_count(df, year, severity_status, 'Accident_Severity', f'# of {severity_status} Accidents')
        with col2:    
            display_casualties_count(df, year, severity_status, 'Number_of_Casualties', f'# of {severity_status} Accidents Casualties')
        with col3:
            st.subheader(f'Year: {year}')
        with col4:
            st.subheader( f'Severity Status: {severity_status}')

        display_map(df,year,severity_status)

    elif selected=='Visualizations':
        #image1 = Image.open('assets/accs_with_time.png')
        #image2 = Image.open('assets/accs_with_time2.png')
        #image3 = Image.open('assets/accs_with_time3.png')
        image4 = Image.open('assets/accs_with_time4.png')
        image5 = Image.open('assets/accs_with_time5.png')
        image6 = Image.open('assets/accs_with_time6.png')
        image7 = Image.open('assets/accs_with_time7.png')
  

        images=[image4,image5,image6,image7]
        titles=['By Year', 'By Month', 'By Quarter', 'By Hours']

        for title,image in zip(titles,images):
            st.subheader(title)
            st.image(image)
            #st.write('\n')
    #st.write(df.sample(20))
    #st.write(df.shape)
    #st.write(df.columns)


if __name__ == "__main__":
    main()

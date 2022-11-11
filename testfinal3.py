import streamlit as st
import pandas as pd
import folium as flm
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from PIL import Image

APP_TITLE='Predicting RTC severity using Machine Learning'

def display_accidents_count(df, year, severity_status, accident_severity,pforce, metric_title):
    df=df[(df['Year']== year)]
    if pforce:
        df=df[df['Police_Force']==pforce]
        df.drop_duplicates(inplace=True)
        total=df[accident_severity].count()
        #st.metric(metric_title,'{:,}'.format(total))
    if severity_status:
        df=df[df['Accident_Severity']==severity_status]
        df.drop_duplicates(inplace=True)
        total=df[accident_severity].count()
        st.metric(metric_title,'{:,}'.format(total))

def display_casualties_count(df, year, severity_status, no_of_casualties ,pforce, metric_title):
#def display_casualties_count(data, year,severity_status, pforce , metric_title):

    df=df[(df['Year']== year)]
    if pforce:
        df=df[df['Police_Force']==pforce]
        df.drop_duplicates(inplace=True)
        total=df[no_of_casualties].sum()
        #st.metric(metric_title,'{:,}'.format(total))
    if severity_status:
        df=df[df['Accident_Severity']==severity_status]
        df.drop_duplicates(inplace=True)
        total=df[no_of_casualties].sum()
        st.metric(metric_title,'{:,}'.format(total))


# def display_map(df,year,severity_status):
#     df=df[df['Year']==year]

#     if severity_status:
#         df=df[df['Accident_Severity']==severity_status]

#         dfmap=df[["Latitude","Longitude"]]
#         dfmap= dfmap.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

#     st.map(dfmap,zoom=5)

def display_year(df,year,metric_title):
    st.metric(metric_title,'{:}'.format(year))

def display_severity_status(df,severity_status, metric_title):
    st.metric(metric_title,'{:}'.format(severity_status))

def map_rtc(data, year, pforce, severity):
    cond = (data['Year'] == year) & (data['Police_Force'] == pforce) & (data['Accident_Severity'] == severity)

    lat = data[cond]['Latitude'].tolist()
    lon = data[cond]['Longitude'].tolist()
    nam = data[cond]['Police_Force'].tolist()
    sev = data[cond]['Accident_Severity'].tolist()
    cas = data[cond]['Number_of_Casualties'].tolist()
    veh = data[cond]['Number_of_Vehicles'].tolist()
    # dat = data[cond]['Date'].tolist()

    def color_producer(status):
        if 'Slight' in status:
            return 'green'
        elif 'Serious' in status:
            return 'blue'
        else:
            return 'orange'

    html = '''<h4>Collision Information</h4>
    <b>%s</b> <br /><br />
    <b>Severity: </b> %s <br />
    <b>Casualties: </b> %s <br />
    <b>Vehicles: </b> %s
    '''
    map = flm.Map(location=[lat[0], lon[0]], zoom_start=10, scrollWheelZoom=False)

    fg = flm.FeatureGroup(name='My V Map')

    for lt, ln, nm, st, ca, ve in zip((lat), (lon), (nam), (sev), (cas), (veh)):
        iframe = flm.IFrame(html = html % ((nm), (st), (ca), (ve)), height = 165)
        popup = flm.Popup(iframe, min_width=200, max_width=500)
        fg.add_child(flm.CircleMarker(location = [lt, ln], popup = (popup), fill_color=color_producer(st), color='None', radius=15, fill_opacity = 0.7))
        map.add_child(fg)

    st_map = st_folium(map, width=1600)
def main():
    st.set_page_config(page_title='Omdena Liverpool', layout='wide')

# Colors:
# Blue = #182D40
# Light Blue = #82a6c0
# Green = # 4abd82

    st.markdown(
    """
    <style>
    .block-container.css-18e3th9.egzxvld2 {
    padding-top: 0;
    }
    header.css-vg37xl.e8zbici2 {
    background: none;
    }
    span.css-10trblm.e16nr0p30 {
    text-align: center;
    color: #2c39b1;
    }
    .css-1dp5vir.e8zbici1 {
    background-image: linear-gradient(
        90deg, rgb(130 166 192), rgb(74 189 130)
        );
    }
    .css-tw2vp1.e1tzin5v0 {
    gap: 10px;
    }
    .css-50ug3q {
    font-size: 1.2em;
    font-weight: 600;
    color: #2c39b1;
}
    </style>
    """,
    unsafe_allow_html=True
    )

    col1, col2 = st.columns((1, 3))
    with col1:
        st.image("https://github.com/liskibruh/streamlit-dashboard-RTC/blob/main/assets/omdenaliverpoollogo.png?raw=true")
    with col2:
        st.image("https://raw.githubusercontent.com/liskibruh/streamlit-dashboard-RTC/main/assets/accidents1104x271.png")
    st.title(APP_TITLE)
    st.write('Over the last few years improvements to roads in the UK have been implemented across the country in order to create a safer roading system with some great effect.  \nThe number of **road traffic collisions** are reported to be in decline.  \nUsing datasets from the Department of Transport, we hope to be able to uncover the probability of the severity of a collision.')
    ## DATA
    df=pd.read_parquet('data/full_accident_data_time_series.parquet')
    year=2006
    severity_status='Serious'
    #accident_severity='Accident_Severity'  
    #metric_title=f'# of {severity_status} Accidents'
    
    # st.write(df.sample(1))
    # st.write(len(df['Police_Force'].unique()))
    # st.write(df.columns)
    # st.write(df['Police_Force'].value_counts())
    
    with st.sidebar:
        selected=option_menu(
            menu_title="Main Menu",
            options=['Accidents','Visualizations', 'About']
        )

    if selected=='Accidents':
        year_list=list(df['Year'].unique())
        year_list.sort()
        year=st.sidebar.selectbox('Year_x',year_list,len(year_list)-1)
        pforce_list = list(df['Police_Force'].unique())
        pforce_list.sort()
        pforce = st.sidebar.selectbox('Police Force', pforce_list, len(pforce_list) -1)
        severity_status=st.sidebar.radio('Severity Status', ['Slight','Serious','Fatal'])
        #st.write(year_list)
        #st.subheader(f'Year: {year}')
        #st.subheader(f'Severity Status: {severity_status}')
        #st.subheader('Road Accidents Facts')
        col1,col2,col3,col4=st.columns(4)
        with col1:
            #display_accidents_count(df, year, severity_status, 'Accident_Severity', f'# of {severity_status} Accidents')
            display_accidents_count(df, year, severity_status, 'Accident_Severity', pforce, '# of Accidents')
            #display_accidents_count(df, year, severity_status,pforce, '# of Accidents')


        with col2:
            #display_casualties_count(df, year, severity_status, 'Number_of_Casualties', f'# of {severity_status} Accident Casualties')
            display_casualties_count(df, year, severity_status, 'Number_of_Casualties',pforce, '# of Casualties')
            #display_casualties_count(df, year, severity_status,pforce, '# of Casualties')

        #with col3:
         #   st.subheader(f'Year: {year}')
        #with col4:
         #   st.subheader( f'Severity Status: {severity_status}')
        with col3:
            display_year(df,year,'Year')#, f'Year{year}')
        with col4:
            display_severity_status(df,severity_status, 'Severity Status')

        map_rtc(df, year, pforce, severity_status)

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
            
    elif selected=='About':
        st.markdown('## Project Overview')
        st.markdown('Over the last few years improvements to roads in the UK have been implemented across the country in order to create a safer roading system with some great effect.')
        st.markdown('The number of RTCs or road traffic collisions are reported to be in decline.')
        st.markdown('However there still seems to be a rise in severe and fatal collisions.')
        st.markdown('Using datasets from the Department of Transport, we hope to be able to uncover the probability of the severity of a collision.')
        st.markdown('Using Data Science we will develop and deploy a machine learning model in an effort to predict RTC severity:')
        st.markdown('- Preprocessing')
        st.markdown('- Exploratory Data Analysis')
        st.markdown('- Feature Engineering')
        st.markdown('- Modeling')
        st.markdown('- Machine Learning')
        st.markdown('The project has been broken down into six pipelines:')
        st.markdown('1. Data Engineering')
        st.markdown('2. Group 1 Predicting RTC Severity')
        st.markdown('3. Group 2 Geospatial Heatmap')
        st.markdown('4. Group 3 Time Series Analysis')
        st.markdown('5. Group 4 Vehicle Analysis and Predictions')
        st.markdown('6. Solution Deployment')
        st.markdown('**Pipeline 1** prepares the datasets for groups 1 - 4')
        st.markdown('**Pipelines 2 - 5** will run concurrently and have three tasks:')
        st.markdown('- EDA')
        st.markdown('- Feature Engineering')
        st.markdown('- Model Development and Evaluation')
        st.markdown('**Pipeline 6** will bring together the models and create the solution to be deployed.')
        st.markdown('Each Pipeline will produce a Jupyter notebook, based on the findings of each of the team members notebooks, for their task.')
        st.markdown('The task lead will then produce a combined notebook, being passed on to the next task until completion of all three tasks.')
        st.markdown('The notebooks will be published on the Omdena Liverpool GitHub site.')
    #st.write(df.sample(20))
    #st.write(df.shape)
    #st.write(df.columns)


if __name__ == "__main__":
    main()

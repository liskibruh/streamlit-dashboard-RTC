import streamlit as st
import pandas as pd
import folium as flm
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from PIL import Image

def display_accidents_count(
        df_accident, year, severity_status, accident_severity, metric_title
        ):
    df_accident = df_accident[(df_accident['year'] == year)]
    if severity_status:
        df_accident = df_accident[df_accident['accident_severity'] == severity_status]
        df_accident.drop_duplicates(inplace=True)
        total = df_accident[accident_severity].count()
        st.metric(metric_title, '{:,}'.format(total))


def display_casualties_count(
        df_accident, year, severity_status, no_of_casualties, metric_title
        ):
    df_accident = df_accident[(df_accident['year'] == year)]
    if severity_status:
        df_accident = df_accident[df_accident['accident_severity'] == severity_status]
        df_accident.drop_duplicates(inplace=True)
        total = df_accident[no_of_casualties].sum()
        st.metric(metric_title, '{:,}'.format(total))

def map_rtc(data, year, district):
    cond = (data['year'] == year) & (data['local_authority_(district)'] == district)

    lat = data[cond]['latitude'].tolist()
    lon = data[cond]['longitude'].tolist()
    nam = data[cond]['local_authority_(district)'].tolist()
    sev = data[cond]['accident_severity'].tolist()
    cas = data[cond]['number_of_casualties'].tolist()
    veh = data[cond]['number_of_vehicles'].tolist()
    dat = data[cond]['date'].tolist()

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
    <b>Vehicles: </b> %s <br />
    <b>Date: </b> %s
    '''
    map = flm.Map(location=[lat[1], lon[1]], zoom_start=12, scrollWheelZoom=False)
    
    fg = flm.FeatureGroup(name='My V Map')

    for lt, ln, nm, st, ca, ve, da in zip((lat), (lon), (nam), (sev), (cas), (veh), (dat)):
        iframe = flm.IFrame(html = html % ((nm), (st), (ca), (ve), (da)), height = 165)
        popup = flm.Popup(iframe, min_width=200, max_width=500)
        fg.add_child(flm.CircleMarker(location = [lt, ln], popup = (popup), fill_color=color_producer(st), color='None', radius=15, fill_opacity = 0.7))
        map.add_child(fg)

    st_map = st_folium(map, width=1200)

def main():
    st.set_page_config(layout='wide')
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
    .css-1dp5vir.e8zbici1 {
    background-image: linear-gradient(
        90deg, rgb(130 166 192), rgb(74 189 130)
        );
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    logo_url = 'https://tinyurl.com/244z8sdr'
    headerimg_url = 'https://tinyurl.com/2csbwggj'
    # APP_TITLE = 'Predicting RTC severity using Machine Learning'
    col1, col2 = st.columns((1, 3))
    with col1:
        st.image(logo_url)
    with col2:
        st.image(headerimg_url)
    # st.title(APP_TITLE)
    st.markdown(
        "<h1 style='text-align:center; color: #3a469d;'>Predicting RTC severity using Machine Learning</h1>",
        unsafe_allow_html=True
    )
    st.write('Over the last few years improvements to roads in the UK have been implemented across the country in order to create a safer roading system with some great effect.  \nThe number of **road traffic collisions** are reported to be in decline.  \nUsing datasets from the Department of Transport, we hope to be able to uncover the probability of the severity of a collision.')
    # DATA
    df_accident = pd.read_csv('data/accident_data.csv')
    df_accident.columns= df_accident.columns.str.strip().str.lower()
    df_accident.columns = df_accident.columns.str.replace('-', '_')
    # df_accident.columns = df_accident.columns.str.replace('(', '')
    # df_accident.columns = df_accident.columns.str.replace(')', '')
    year = 2006
    severity_status = 2


    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=['Accidents', 'Visualizations', 'About']
        )

    if selected == 'Accidents':
        year_list = list(df_accident['year'].unique())
        year_list.sort()
        year = st.sidebar.selectbox('Year', year_list, len(year_list) -1)
        district_list = list(df_accident['local_authority_(district)'].unique())
        district_list.sort()
        district = st.sidebar.selectbox('District', district_list, len(district_list) -1)
        severity_status=st.sidebar.radio('Severity Status', ['Slight','Serious','Fatal'])
        # st.write(year_list)
        st.subheader(f'Year: {year}')
        st.subheader(f'Severity Status: {severity_status}')
        # st.subheader('Road Accidents Facts')

        col1, col2, col3 = st.columns(3)
        with col1:
            display_accidents_count(
                df_accident, year, severity_status,
                'accident_severity', f'# of {severity_status} Accidents'
                )
        with col2:
            display_casualties_count(
                df_accident, year, severity_status,
                'number_of_casualties',
                f'# of {severity_status} Accidents Casualties'
                )
        with col3:
            st.write('Add Vehicle count Here')

        map_rtc(df_accident, year, district)

# st.write(df_accident.sample(20))
# st.write(df_accident.shape)
# st.write(df_accident.columns)


if __name__ == "__main__":
    main()

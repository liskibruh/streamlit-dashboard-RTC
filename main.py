import streamlit as st
import pandas as pd
import folium as flm
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import cufflinks

APP_TITLE = 'Predicting RTC severity using Machine Learning'


def display_accidents_count(
    df, year, severity_status, accident_severity, pforce, metric_title
):
    df = df[(df['Year'] == year)]
    if pforce:
        df = df[df['Police_Force'] == pforce]
        df.drop_duplicates(inplace=True)
        total = df[accident_severity].count()
        # st.metric(metric_title,'{:,}'.format(total))
    if severity_status:
        df=df[df['Accident_Severity'] == severity_status]
        df.drop_duplicates(inplace=True)
        total=df[accident_severity].count()
        st.metric(metric_title, '{:,}'.format(total))


def display_casualties_count(
    df, year, severity_status, no_of_casualties, pforce, metric_title
):
    df = df[(df['Year'] == year)]
    if pforce:
        df = df[df['Police_Force'] == pforce]
        df.drop_duplicates(inplace=True)
        total = df[no_of_casualties].sum()

    if severity_status:
        df = df[df['Accident_Severity'] == severity_status]
        df.drop_duplicates(inplace=True)
        total = df[no_of_casualties].sum()
        st.metric(metric_title, '{:,}'.format(total))


def display_year(df, year, metric_title):
    st.metric(metric_title, '{:}'.format(year))


def display_severity_status(df, severity_status, metric_title):
    st.metric(metric_title, '{:}'.format(severity_status))


def map_rtc(data, year, pforce, severity):
    cond = (
        data['Year'] == year
    ) & (
        data['Police_Force'] == pforce
    ) & (
        data['Accident_Severity'] == severity
    )

    lat = data[cond]['Latitude'].tolist()
    lon = data[cond]['Longitude'].tolist()
    nam = data[cond]['Police_Force'].tolist()
    sev = data[cond]['Accident_Severity'].tolist()
    cas = data[cond]['Number_of_Casualties'].tolist()
    veh = data[cond]['Number_of_Vehicles'].tolist()
    dat = data[cond]['Date'].tolist()
    tim = data[cond]['Time'].tolist()

    def color_producer(status):
        if 'Slight' in status:
            return 'green'
        elif 'Serious' in status:
            return 'blue'
        else:
            return 'orange'

    html = '''<h3>Collision Information</h3>
    <p><b>%s</b></p>
    <table style="width:250px">
    <tr>
    <td><b>Severity: </b></td>
    <td><b>%s</b></td>
    </tr>
    <tr>
    <td><b>Casualties: </b></td>
    <td><b>%s</b></td>
    </tr>
    <tr>
    <td><b>Vehicles: </b></td>
    <td><b>%s</b></td>
    </tr>
    <tr>
    <td><b>Date: </b></td>
    <td><b>%s</b></td>
    </tr>
    <tr>
    <td><b>Time: </b></td>
    <td><b>%s</b></td>
    </tr>
    </table>
    '''
    map = flm.Map(
        location=[lat[0], lon[0]], zoom_start=10, scrollWheelZoom=False
    )

    fg = flm.FeatureGroup(name='My V Map')

    for lt, ln, nm, st, ca, ve, da, ti in zip(
        (lat), (lon), (nam), (sev), (cas), (veh), (dat), (tim)
    ):
        iframe = flm.IFrame(
            html = html % ((nm), (st), (ca), (ve), (da), (ti)), height = 185
        )
        popup = flm.Popup(iframe, min_width=275, max_width=500)
        fg.add_child(
            flm.CircleMarker(
                location=[lt, ln], popup=(popup),
                fill_color=color_producer(st), color='None',
                radius=15, fill_opacity=0.7
            )
        )
        map.add_child(fg)

    st_map = st_folium(map, width=1600)
    return st_map

@st.cache
def get_data(url):
    df = pd.read_parquet(url)

    return df


def main():
    st.set_page_config(page_title='Omdena Liverpool', layout='wide')

# Colors:
# Blue = #182D40
# Light Blue = #82a6c0
# Green = #4abd82

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
    .row-widget.stSelectbox {
    padding: 10px;
    background: #ffffff;
    border-radius: 7px;
    }
    .row-widget.stRadio {
    padding: 10px;
    background: #ffffff;
    border-radius: 7px;
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

    # Load the DATA
    url = 'data/full_accident_data_time_series.parquet'
    df = get_data(url)
    year = 2006
    severity_status = 'Serious'

    # st.write(df.sample(1))
    # st.write(df['Date'])
    # st.write(len(df['Police_Force'].unique()))
    # st.write(df.columns)
    # st.write(df.shape)

    # Add a sidebar for navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=['Accidents', 'Visualizations', 'About']
        )
    # Crete pages
    if selected == 'Accidents':
        year_list = list(df['Year'].unique())
        year_list.sort()
        year = st.sidebar.selectbox(
            'Year', year_list, len(year_list) - 1
        )
        pforce_list = list(df['Police_Force'].unique())
        pforce_list.sort()
        pforce = st.sidebar.selectbox(
            'Police Force', pforce_list, len(pforce_list) - 1
        )
        severity_status = st.sidebar.radio(
            'Severity Status', ['Slight','Serious', 'Fatal']
        )

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            display_year(df,year,'Year')#, f'Year{year}')

        with col2:
            display_accidents_count(
                df, year, severity_status, 'Accident_Severity',
                pforce, '# of Accidents'
            )

        with col3:
            display_casualties_count(
                df, year, severity_status, 'Number_of_Casualties',
                pforce, '# of Casualties'
            )

        with col4:
            display_severity_status(
                df, severity_status, 'Severity Status'
            )

        map_rtc(df, year, pforce, severity_status)

    elif selected == 'Visualizations':
        image4 = Image.open('assets/accs_with_time4.png')
        image5 = Image.open('assets/accs_with_time5.png')
        image6 = Image.open('assets/accs_with_time6.png')
        image7 = Image.open('assets/accs_with_time7.png')

        # images = [image4, image5, image6, image7]
        # titles = ['By Year', 'By Month', 'By Quarter', 'By Hours']

        # for title, image in zip(titles, images):
        #     st.subheader(title)
        #     st.image(image)
        st.title('By Year')
        st.markdown('We can see that from 2005 we have a healthy decline in **RTCs**')
        st.markdown('However both **serious** and **Fatal** **RTCs** have either plateaued or are on the rise')
        st.image(image4)
        st.title('By Month')
        st.markdown('Our monthly data differs from severity to severity.')
        st.markdown('The **RTCs** for **Fatal** peak in August, October and November.')
        st.markdown('The **RTCs** for **Serious** peak in July.')
        st.markdown('The **RTCs** for **Slight** peak in November.')
        st.image(image5)
        st.title('By Quarter')
        st.markdown('Both **Fatal** and **Slight** **RTCs** peak in Quarter 4.')
        st.image(image6)
        st.title('By Hours')
        st.markdown('All of our **RTCs** show an increase at rush hours.')
        st.image(image7)

    elif selected == 'About':
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


if __name__ == "__main__":
    main()

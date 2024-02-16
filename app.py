import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import streamlit.components.v1 as components
from bs4 import BeautifulSoup as bs
import pandas as pd
from requests import get
import base64
import matplotlib.pyplot as plt

st.markdown("<h1 style='text-align: left; color: black;'> COINAFRICA DATA SCRAPER APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs simple webscraping of data from Coinafrique-dakar over multiples pages!
* **Python libraries:** base64, pandas, streamlit, requests, bs4, plotly.express, matplotlib.pyplot, streamlit.components.v1
* **Data source:** [Coinafrique-Dakar](https://sn.coinafrique.com/).
""")

# Fonction Background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('img_file2.jpg') 


# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1


### load data
def load_data():
    Chaussures_Enfants = pd.read_csv('Chaussures_Enfants.csv', encoding='latin-1', sep=";")
    Chaussures_Hommes  = pd.read_csv('Chaussures_Hommes.csv', encoding='latin-1', sep=";")
    Vetements_Enfants  = pd.read_csv('Vetements_enfants.csv', encoding='latin-1', sep=";")
    Vetements_Hommes   = pd.read_csv('Vetements_Hommes.csv', encoding='latin-1', sep=";")
    return Chaussures_Enfants, Chaussures_Hommes, Vetements_Enfants, Vetements_Hommes


### Sidebar ###

def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Menu",  # required
                options=["Scraper data", "Download data", "Dashbord", "Note App"],  # required
                icons=["arrow-repeat", "download", "bar-chart", "card-checklist"],  # optional
                menu_icon="list",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Scraper data", "Download data", "Dashbord", "Note App"],  # required
                icons=["arrow-repeat", "download", "bar-chart", "card-checklist"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 3:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Scraper data", "Download data", "Dashbord", "Note App"],  # required
            icons=["arrow-repeat", "download", "bar-chart", "card-checklist"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 4:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Scraper data", "Download data", "Dashbord", "Note App"],  # required
            icons=["arrow-repeat", "download", "bar-chart", "card-checklist"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected


#### Page pour scraper la fata ####

def scraper_data(url, limit):
    df = pd.DataFrame()
    obj = {}
    for p in range(1, limit + 1):
        resp = get(url)
        soup = bs(resp.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                type_habits = container.find('p', class_ = 'ad__card-description').text
                prix = container.find('p', class_ = 'ad__card-price').text.replace('CFA', '').replace(' ', '')
                adresse = container.find('p', class_ = 'ad__card-location').find('span').text
                image_lien = container.find('img', class_ = 'ad__card-img')['src']
                
                obj = {
                    'type_habits': type_habits,
                    'prix': int(prix),
                    'adresse': adresse,
                    'image_lien': image_lien
                    }
            except:
                pass
            data.append(obj)


        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0).reset_index(drop = True)
    
    return df

def scraper_data_beautifulsoup():
    st.title("Scrape Data")

    limit = st.number_input("Numero de pages à scraper", min_value=1, step=1)
    urls = [
        {
            "title":"Vetements homme",
            "url":f"https://sn.coinafrique.com/categorie/vetements-homme?page={limit}",
            "key":1,
            "key1":101
        }, 
        
        {
            "title":"Chaussures homme",
            "url":"https://sn.coinafrique.com/categorie/chaussures-homme?page={limit}",
            "key":2,
            "key1":102
        },
        {
            "title":"Vetements enfant",
            "url":"https://sn.coinafrique.com/categorie/vetements-enfants?page={limit}",
            "key":3,
            "key1":103
        },
        {
            "title":"Chaussures enfant",
            "url":"https://sn.coinafrique.com/categorie/chaussures-enfants?page={limit}",
            "key":4,
            "key1":104
        }
    ]
    for url in urls:

        if st.button(url['title'], url['key1']):
            # Scraper les données
            scraped_data = scraper_data(url['url'], limit)
            
            # Afficher les données scrappées dans un dataframe pandas
            if scraped_data is not None:
                st.write(scraped_data)
                
                st.markdown("""
                <style>
                div.stButton {text-align:center}
                </style>""", unsafe_allow_html=True)
                title = 'Vetements_Hommes'
                csv = convert_df(scraped_data)

                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=url['title'].replace(' ', '_')+'.csv',
                    mime='text/csv',
                    key = url['key'])
                
            else:
                st.write("Aucune donnée n'a été scrappée.")


#### Page download datas ####

def download_data():
    st.title(f"Download Scarped data")

    Chaussures_Enfants, Chaussures_Hommes, Vetements_Enfants,Vetements_Hommes = load_data()

    load(Chaussures_Enfants, 'Chaussures_Enfants', '1', '101')
    load(Chaussures_Hommes, 'Chaussures_Hommes', '2', '102')
    load(Vetements_Enfants, 'Vetements_enfants', '3', '103')
    load(Vetements_Hommes, 'Vetements_Hommes', '4', '104')


@st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

def load(dataframe, title, key, key1) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key1):
        # st.header(title)

        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = convert_df(dataframe)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key = key)


#### Page Dashbord ####
def dashbord():
    st.title("Dashbord of the data")
    Chaussures_Enfants, Chaussures_Hommes, Vetements_Enfants,Vetements_Hommes = load_data()

    # Types de chaussures pour enfant en fonction du prix
    st.subheader('Types de chaussures pour enfant en fonction du prix')
    fig = px.scatter(Chaussures_Enfants, x='type_chaussures', y='prix', color='type_chaussures', hover_name='type_chaussures')
    st.plotly_chart(fig)

    # Vêtements pour enfant en fonction du prix
    st.subheader('Vêtements pour enfant en fonction du prix')
    fig = px.bar(Vetements_Enfants, x='types_habits', y='prix', color='types_habits', hover_name='types_habits')
    st.plotly_chart(fig)

    # Types de chaussures pour homme en fonction du prix
    st.subheader('Types de chaussures pour homme en fonction du prix')
    fig = px.scatter(Chaussures_Hommes, x='type_chaussures', y='prix', color='type_chaussures', hover_name='type_chaussures')
    st.plotly_chart(fig)

    # Vêtements pour homme en fonction du prix
    st.subheader('Vêtements pour homme en fonction du prix')
    fig = px.bar(Vetements_Hommes, x='type_habits', y='prix', color='type_habits', hover_name='type_habits')
    st.plotly_chart(fig)


#### Page note application ####

def note_application():
    st.title("Noter l'application")

    # URL du formulaire KoboldTools
    url_formulaire_koboldtools = "https://ee.kobotoolbox.org/i/N6H3cm1G"

    # Affichage de l'iframe
    st.components.v1.iframe(url_formulaire_koboldtools, height=900)



### MAIN
selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "Scraper data":
    scraper_data_beautifulsoup()
if selected == "Download data":
    download_data()
if selected == "Dashbord":
   dashbord()
if selected == "Note App":
   note_application()
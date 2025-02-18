## Planet Generator

import streamlit as st
import pandas as pd
from PlanetGeneratorFunctions import newplanet, planet_graphics,convert_df_to_csv,generate_pois

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stButton]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        p { line-height: 1 !important; }
        body {
            background-color: black;
            color: #00FF00;
            font-family: 'Courier New', Courier, monospace;
        }
        .stApp {
            background-color: black;
            color: #00FF00;
        }
        p, h1, h2, h3, h4, h5, h6 {
            color: #00FF00 !important;
        }
        .terminal-cursor {
            display: inline-block;
            width: 10px;
            background-color: #00FF00;
            animation: blink 1s steps(2, start) infinite;
            margin-left: 2px;
        }
        @keyframes blink {
            to { visibility: hidden; }
        }
        [data-testid="stSidebar"] {
            background-color: black;
        }
    </style>
    """, unsafe_allow_html=True
)

# Set app title
st.title("Galactic Cartographers")

# Generate initial planet if init was not stored in session state
# if init exists in session state do not run this code.
if "init" not in st.session_state:
    # planetdb holds a record of all planets that have been created in a session as well as the randomseed used to generate graphics.
    planetdb=pd.DataFrame(columns=["name","type","size","features","icecaps","settlement size","settlements","development","law",
                                "price modifier","distance to star","avg temperature (c)","atmosphere","atomosphere notes",
                                "gravity","hours in day","graphicseed","record id"])
    planet_dict,st.session_state['planetdb']=newplanet(planetdb,"Any","Any",0,0)
    planet_fig,planet_map_poi,planet_map,pois=planet_graphics(planet_dict["type"],planet_dict["icecaps"],planet_dict["size"],planet_dict["graphicseed"])
    poidict=generate_pois(pois,planet_dict["type"])

# Store initial planet in session states
if "init" not in st.session_state:
    st.session_state["init"]=1
if "poimap" not in st.session_state:
    st.session_state["poimap"]=planet_map_poi
if "map" not in st.session_state:
    st.session_state["map"]=planet_map
if "planet_fig" not in st.session_state:
    st.session_state["planet_fig"]=planet_fig
if "planet_dict" not in st.session_state:
    st.session_state["planet_dict"]=planet_dict
    print("Added to Session State")
if "planet_poi" not in st.session_state:
    st.session_state["planet_poi"]=poidict
if "planetdb" not in st.session_state:
    st.session_state["planetdb"]=planetdb

with st.sidebar:
    st.image("https://i.imgur.com/PCS1XPq.png")
    planettype=st.selectbox("Planet Type to Retrieve",("Any","Desert","Jungle","Rocky","Oceanic","Crystal","Frozen","Volcanic","Steppe","Gas Giant"),)
    planetsize=st.selectbox("Planet Size to Retrieve",("Any","Gas Giant Moon","Dwarf","Small","Medium","Large","Giant"),)
    planetseed=st.text_input("Planet Record ID")
    if(st.button("Retrieve New World")):
        planet_dict,st.session_state['planetdb']=newplanet(st.session_state['planetdb'],planettype,planetsize,0,planetseed)
        planet_fig,planet_map_poi,planet_map,pois=planet_graphics(planet_dict["type"],planet_dict["icecaps"],planet_dict["size"],planet_dict["graphicseed"])
        poidict=generate_pois(pois,planet_dict["type"])
        st.session_state["poimap"]=planet_map_poi
        st.session_state["map"]=planet_map
        st.session_state["planet_fig"]=planet_fig
        st.session_state["planet_dict"]=planet_dict
        st.session_state["planet_poi"]=poidict
    poi_onoff=st.toggle("Show POIs")

    st.write("Welcome to the Department of Galactic Cartography, an online catalog of nearly limitless worlds, surveyed or not.")
    st.write("-------------------------------")
    st.write("This was written to create planets for a Savage Worlds game, but with the idea of it being 100% system agnostic.")
    st.write("Scroll down to see a map view of the world, and you can use the image controls to save images of the planet globe and map.") 
    st.write("Be sure to set them to full screen before you capture them, especially the map.")
    st.write("Below the planetary map, is a second map displaying planetary sites to be explored.")
    #st.write("-------------------------------")
    #st.image("https://i.imgur.com/kv7vuDb.png")


tab1,tab2=st.tabs(["Planet Readout","Previous Exploration"])

tab1.header(st.session_state['planet_dict']['name'])

config_globe = {'displayModeBar': True,
        'use_container_width':False}

with tab1:
    col1, col2 = st.columns(2,vertical_alignment="top",border=True)
    for x in st.session_state["planet_dict"]:
        if x!="name" and x!="graphicseed" and x!="orbit":
                with col1:
                    st.write (f"{x.title()}: {st.session_state['planet_dict'][x]}")
    with col2:
        col2.plotly_chart(st.session_state["planet_fig"],config=config_globe)
tab1.write('## Planetary Map View')
if poi_onoff:
    tab1.plotly_chart(st.session_state["poimap"])
else:
    tab1.plotly_chart(st.session_state["map"])
#st.header('Planetary Sites View')

tab1.write("## Planetary Sites")
if len(st.session_state["planet_poi"])>0:
    for x in range(0,len(st.session_state["planet_poi"])):
        tab1.write(f"{x+1}: {st.session_state['planet_poi'][x]['name']} ({st.session_state['planet_poi'][x]['type']})")
else:
    tab1.write("Nothing of Interest")

tab2.write("## Previously Viewed")
tab2.dataframe(st.session_state['planetdb'])

tab2.download_button(
  label="Download Planetary Records",
  data=convert_df_to_csv(st.session_state['planetdb']),
  file_name='planets.csv',
  mime='text/csv',
)


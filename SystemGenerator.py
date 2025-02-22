import plotly.graph_objects as go
import numpy as np
import random
import pandas as pd
import os
import streamlit as st
from PlanetGeneratorFunctions import newplanet,planet_graphics

def convert_df_to_csv(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

def ellipse_arc(x_center=0, y_center=0, a=1, b =1, start_angle=0, end_angle=2*np.pi, N=100, closed= False):
    t = np.linspace(start_angle, end_angle, N)
    x = x_center + a*np.cos(t)
    y = y_center + b*np.sin(t)
    path = f'M {x[0]}, {y[0]}'
    for k in range(1, len(t)):
        path += f'L{x[k]}, {y[k]}'
    if closed:
        path += ' Z'
    return path

def generate_system(seed=0):
    #print(seed)
    if seed==0 or seed is None or seed=="":
        random_data = os.urandom(8)
        seed = int(int.from_bytes(random_data, byteorder="big")/1000000000000)
        seed=f"sys-svrn-{seed}"
        random.seed(str(seed))
    else:
        #print(f"Generating {seed}")
        random.seed(seed)
    systemdf=pd.DataFrame()

    prefixes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Theta", "Omicron", 
            "Nova", "XJ", "YV", "ZX", "Upsilon", "Tau", "Sigma", "Lambda", "Kappa"]

    # Core name parts for variety
    name_parts = ["Orion", "Draconis", "Vega", "Nyx", "Seraphis", "Tarsis", "Solari", "Nebulus", 
              "Vorlax", "Eldara", "Typhon", "Sirius", "Hyperion", "Zephyrus", "Callidus", "Lyra", 
              "Polaris", "Aetheris", "Icarus", "Prometheus", "Cygni", "Rigel", "Andara"]

    # Expanded suffixes for uniqueness
    suffixes = ["Prime", "Minor", "Major", "Nexus", "Core", "Outpost",
            "Sector", "Expanse", "Horizon", "Bastion", "Stronghold", "Citadel", "Terminus", 
            "Observatory", "Harbinger", "Apex", "Sentinel", "Pinnacle", "Echelon", "Periphery", 
            "Zenith", "Dominion", "Frontier", "Ascendancy", "Anomaly", "Haven", "Sanctuary"]


    prefix = random.choice(prefixes)
    core_name = random.choice(name_parts)
    suffix = random.choice(suffixes) if random.random() > 0.3 else ""  # Optional suffix

    systemname=f"{prefix} {core_name} {suffix}"

    startypes = [
        "O-type",  # Hot, massive, and blue
        "B-type",  # Blue, very luminous
        "A-type",  # White, hot, and bright
        "F-type",  # Yellow-white, moderate temperature
        "G-type",  # Yellow, like our Sun
        "K-type",  # Orange, cooler than the Sun
        "M-type",  # Red dwarfs, most common
        "L-type",  # Brown dwarfs, very cool
        "T-type",  # Cooler brown dwarfs
        "Y-type",  # The coolest brown dwarfs
        "Wolf-Rayet",  # Extremely hot, massive, and losing mass
        "Red Giant",  # Late-stage, expanded star
        "White Dwarf"
    ]
    star_sizes = {
        "O-type": 1200,        # Massive, up to 10x the Sun's radius
        "B-type": 1000,        # Large, but less than O-type
        "A-type": 800,        # Bigger than the Sun, but not extreme
        "F-type": 500,         # Slightly larger than the Sun
        "G-type": 250,         # Baseline (like our Sun)
        "K-type": 150,         # Slightly smaller than the Sun
        "M-type": 100,          # Red dwarfs, much smaller
        "L-type":90,          # Brown dwarfs, very small
        "T-type": 70,          # Cooler brown dwarfs
        "Y-type": 60,           # The smallest brown dwarfs
        "Wolf-Rayet": 900,    # Massive, but shedding mass
        "Red Giant": 800,     # Can be much larger than the Sun
        "White Dwarf": 60     # Earth-sized remnant
    }

    star_colors = {
        "O-type": "blue",           # Very hot, blue stars
        "B-type": "royalblue",      # Slightly cooler than O-type
        "A-type": "deepskyblue",    # White to blue-white
        "F-type": "lightyellow",      # Yellow-white stars
        "G-type": "gold",           # Sun-like, yellow
        "K-type": "orange",         # Orange-hued stars
        "M-type": "red",            # Red dwarfs
        "L-type": "brown",          # Brown dwarfs
        "T-type": "purple",         # Cooler brown dwarfs with methane absorption
        "Y-type": "darkslategray",  # The coolest brown dwarfs
        "Wolf-Rayet": "hotpink",    # Massive, luminous, often pinkish due to ionized gas
        "Red Giant": "darkred",  # Late-stage, massive red stars
        "White Dwarf": "whitesmoke"
    }

    star_orbits = {
        "O-type": 6,        # Very hot, blue stars
        "B-type": 4,        # Slightly cooler than O-type
        "A-type": 4,        # White to blue-white
        "F-type": 3,        # Yellow-white stars
        "G-type": 1,        # Sun-like, yellow
        "K-type": 0,        # Orange-hued stars
        "M-type": 0,        # Red dwarfs
        "L-type": 0,        # Brown dwarfs
        "T-type": 0,        # Cooler brown dwarfs with methane absorption
        "Y-type": 0,        # The coolest brown dwarfs
        "Wolf-Rayet": 5,    # Massive, luminous, often pinkish due to ionized gas
        "Red Giant": 3,     # Late-stage, massive red stars
        "White Dwarf": 0
    }

    star=random.choice(startypes)

    starcolor=star_colors[star]
    starsize=star_sizes[star]
    minorbit=star_orbits[star]
    #print(minorbit)
    for x in range(minorbit,8):
        orbitrow=[]
        
        planettype=["Any","Any","Any","Any","Any","Any","Any","Any","None","None","Asteroid","Asteroid"]
        outerplanetype=["Any","Any","Any","Any"]
        #planetsize=["Dwarf","Small","Small","Medium","Medium","Medium","Large","Giant"]
        #gasgiantsize=["Giant","Gas Giant","Small Gas Giant"]
        #planetcolor={"Desert":'darkgoldenrod',"Jungle":'darkgreen',"Oceanic":'blue',"Volcanic":'red',"Frozen":'aqua',"Rocky":"brown","Crystal":'purple',"Steppe":"greenyellow","None":"black","Asteroid":"brown","Gas Giant":"pink"}
        #planetdisplaysize={"Dwarf":10,"Small":15,"Medium":25,"Large":35,"Giant":45,"Gas Giant Moon":0.75,"Asteroid":8,"Small Gas Giant":55,"Gas Giant":70}
        if x-minorbit>4:
            type=random.choice(outerplanetype)
        else:
            type=random.choice(planettype)
        #if type=="Gas Giant":
        #    size=np.random.choice(gasgiantsize)
        #else:
        #    size=np.random.choice(planetsize)
        #
        #def newplanet(planetdb,selectedtype="Any",selectedsize="Any",orbitdistance=0,planetseed=0):
        #print(f"Seed being passed to planet: {seed}")
        planetdict,systemdf=newplanet(systemdf,selectedtype=type,orbitdistance=x,systemseed=seed)
        
        #'''
        #orbitrow.append(type)
        #orbitrow.append(planetcolor[type])
        #orbitrow.append(size)
        #orbitrow.append(planetdisplaysize[size])
        #orbitrow.append(orbit)
        #orbitrow.append(x)
        #orbitrow.append(10)
        #'''
        #systemdf.loc[len(systemdf)]=orbitrow
    systemdf["level"]=10
    systemdf["startype"]=star
    systemdf["systemname"]=systemname
    systemdf["system id"]=seed
    fullsystemdf=pd.DataFrame()
    fullsystemdf=systemdf
    #print(fullsystemdf)
    systemdf=systemdf[systemdf["type"]!="None"]
    asteroiddf=systemdf[systemdf["type"]=="Asteroid"]
    #print(f"Star: {star}")
    #print(asteroiddf)
    systemdf=systemdf[systemdf["type"]!="Asteroid"]
    #print(systemdf)
    

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=[0],y=[10],mode='markers',marker=dict(size=starsize+10,color='black',line=dict(color=starcolor,width=2))))
    fig.add_trace(go.Scatter(x=[0],y=[10],mode='markers',marker=dict(size=starsize,color=starcolor)))

    orbitalpaths=[]

    for index,orbitpos in systemdf.iterrows():
        #print(orbitpos["orbit"])
        #fig.add_trace(go.Scatter(x=[0],y=[10],mode='markers',marker=dict(size=525+(orbitpos["orbitposition"]*349),color="rgba(0,0,0,0)",line=dict(color='white',width=0.25))))
        orbitalpaths.append(dict(type="path", path=ellipse_arc(y_center=10,a=orbitpos["orbit"],b=orbitpos["orbit"]-5,N=60),line_color="white",line_width=0.25,line_dash="dot"))

    #print(len(systemdf))
    if (len(systemdf))>0:
        fig.add_trace(go.Scatter(x=systemdf["orbit"],y=systemdf["level"],mode='markers',marker=dict(size=systemdf["plotsize"],color=systemdf["color"],line=dict(color='black'))))
        fig.add_trace(go.Scatter(x=systemdf["orbit"],y=systemdf["level"],mode='markers',text=["test"],textfont=dict(color="white",size=20),marker=dict(size=systemdf["plotsize"],color=systemdf["color"],line=dict(color='black'))))

    for x in range(0,10):
        offsetx=random.uniform(-.25,.25)
        offsety=random.uniform(-2,2)
        offsetangle=random.randint(0,90)
        fig.add_trace(go.Scatter(x=asteroiddf["orbit"]+offsetx,y=asteroiddf["level"]+offsety,mode='markers',marker_symbol="octagon",text=asteroiddf["type"],marker=dict(angle=offsetangle,size=5,color="gray",line=dict(color='black'))))
    for x in range(0,10):
        offsetx=random.uniform(-.25,.25)
        offsety=random.uniform(-2,2)
        offsetangle=random.randint(0,90)
        fig.add_trace(go.Scatter(x=asteroiddf["orbit"]+offsetx,y=asteroiddf["level"]+offsety,mode='markers',marker_symbol="octagon",text=asteroiddf["type"],marker=dict(angle=offsetangle,size=5,color="slategrey",line=dict(color='black'))))

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        width=1024,
        height=600,
        plot_bgcolor="black",
        xaxis=dict(range=[0,100]),
        yaxis=dict(range=[0,20]),
        showlegend=False,
        shapes=orbitalpaths
    )
    return fig,systemdf,fullsystemdf,asteroiddf,seed

st.set_page_config(page_title="System Generator", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

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


if "init" not in st.session_state:
    print("Initalizing...")
    systemdf=pd.DataFrame()
    fullsystemdf=pd.DataFrame()
    fig,systemdf,fullsystemdf,asteroiddf,seed=generate_system()
if "init" not in st.session_state:
    st.session_state["init"]=1

if "systemdf" not in st.session_state:
    st.session_state["systemdf"]=systemdf
if "systemfig" not in st.session_state:
    st.session_state["systemfig"]=fig
if "fullsystemdf" not in st.session_state:
    st.session_state["fullsystemdf"]=fullsystemdf
    print("Added to Session State")
if "asteroiddf" not in st.session_state:
    st.session_state["asteroiddf"]=asteroiddf
if "systemseed" not in st.session_state:
    st.session_state["systemseed"]=seed

print(st.session_state["fullsystemdf"])

# Set app title
st.title("Galactic Cartographers: System View")

with st.sidebar:
    st.image("https://i.imgur.com/PCS1XPq.png")
    systemseed=st.text_input("System ID")
    if(st.button("Retrieve System")):
        st.session_state["systemfig"],st.session_state["systemdf"],st.session_state["fullsystemdf"],st.session_state["asteroiddf"],st.session_state["systemseed"]=generate_system(systemseed)
    st.write("Welcome to the Department of Galactic Cartography, an online catalog of nearly limitless worlds, surveyed or not.")
    st.write("-------------------------------")
    st.write("This was written to build out entire star systems for a Savage Worlds game, but with the idea of it being 100% system agnostic.")
    st.write("Scroll down to see a list of the worlds and their ID.") 
    st.write("Be sure to set them to full screen before you capture the system.")

tab1,tab2=st.tabs(["System View","Planet Explorer"])

config_globe = {'displayModeBar': True,
        'use_container_width':False}
config_map = {'displayModeBar': True,
        'use_container_width':False}


with tab1:
    st.header(f"Star: {st.session_state['fullsystemdf']['systemname'].iloc[0]}")
    st.write(f"Star: {st.session_state['fullsystemdf']['startype'].iloc[0]}")
    st.write(f"System ID: {st.session_state['fullsystemdf']['system id'].iloc[0]}")
    st.plotly_chart(st.session_state["systemfig"],config=config_globe)
    st.dataframe(st.session_state["systemdf"])

with tab2:
    st.header(f"Star: {st.session_state['fullsystemdf']['systemname'].iloc[0]}")
    st.write(f"Star: {st.session_state['fullsystemdf']['startype'].iloc[0]}")
    st.write(f"System ID: {st.session_state['fullsystemdf']['system id'].iloc[0]}")
    choice=st.selectbox("Choose Planet to View",st.session_state["systemdf"]["name"])
    print(choice)
    chosenplanet=st.session_state["systemdf"][st.session_state["systemdf"]["name"]==choice]  # Filter
    if len(chosenplanet)>0:
        planetseed=int(chosenplanet["graphicseed"].iloc[0])
        print(planetseed)
        fig,fig_flat_poi,fig_flat,poinumber=planet_graphics(chosenplanet["type"].iloc[0],chosenplanet["icecaps"].iloc[0],chosenplanet["size"].iloc[0],graphicseed=planetseed)
        col1, col2 = st.columns(2,vertical_alignment="top",border=True)
        planet_dict=chosenplanet.squeeze().to_dict()
        print(planet_dict)
        for x in planet_dict:
            cells_donotplot=["name","graphicseed","orbit","color","plotsize"]
            if x not in cells_donotplot:
                    with col1:
                        st.write (f"{x.title()}: {planet_dict[x]}")
        with col2:
            col2.plotly_chart(fig,config=config_globe)
        st.write('## Planetary Map View')
        poi_onoff=st.toggle("Show POIs")
        if poi_onoff:
            st.plotly_chart(fig_flat_poi)
        else:
            st.plotly_chart(fig_flat)
    else:
        st.write("No planets to display.")

    #tab2.plotly_chart(fig,config=config_globe)
st.download_button(
  label="Download Planetary Records",
  data=convert_df_to_csv(st.session_state["fullsystemdf"]),
  file_name='system.csv',
  mime='text/csv',
)
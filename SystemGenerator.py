import plotly.graph_objects as go
import numpy as np
import random
import pandas as pd
import os
import streamlit as st
from PlanetGenerator import newplanet

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

def generate_system():
    baseorbit=15
    systemdf=pd.DataFrame(columns=["type","color","size","plotsize","orbit","orbitposition","level"])

    random_data = os.urandom(8)
    seed = int(int.from_bytes(random_data, byteorder="big")/1000000000000)
    seed=f"svrn-{seed}"
    random.seed(str(seed))


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
        "O-type": 5,        # Very hot, blue stars
        "B-type": 4,        # Slightly cooler than O-type
        "A-type": 3,        # White to blue-white
        "F-type": 3,        # Yellow-white stars
        "G-type": 0,        # Sun-like, yellow
        "K-type": 0,        # Orange-hued stars
        "M-type": 0,        # Red dwarfs
        "L-type": 0,        # Brown dwarfs
        "T-type": 0,        # Cooler brown dwarfs with methane absorption
        "Y-type": 0,        # The coolest brown dwarfs
        "Wolf-Rayet": 4,    # Massive, luminous, often pinkish due to ionized gas
        "Red Giant": 5,     # Late-stage, massive red stars
        "White Dwarf": 0
    }

    star=random.choice(startypes)

    starcolor=star_colors[star]
    starsize=star_sizes[star]
    minorbit=star_orbits[star]
    print(minorbit)
    for x in range(minorbit,8):
        orbitrow=[]
        planettype=["Desert","Jungle","Oceanic","Volcanic","Frozen","Rocky","Crystal","Steppe","None","None","Asteroid","Asteroid"]
        outerplanetype=["Gas Giant","Gas Giant","Gas Giant","Rocky"]
        planetsize=["Dwarf","Small","Small","Medium","Medium","Medium","Large","Giant"]
        gasgiantsize=["Giant","Gas Giant","Small Gas Giant"]
        planetcolor={"Desert":'darkgoldenrod',"Jungle":'darkgreen',"Oceanic":'blue',"Volcanic":'red',"Frozen":'aqua',"Rocky":"brown","Crystal":'purple',"Steppe":"greenyellow","None":"black","Asteroid":"brown","Gas Giant":"pink"}
        planetdisplaysize={"Dwarf":10,"Small":15,"Medium":25,"Large":35,"Giant":45,"Gas Giant Moon":0.75,"Asteroid":8,"Small Gas Giant":55,"Gas Giant":70}
        if x-minorbit>4:
            type=np.random.choice(outerplanetype)
        else:
            type=np.random.choice(planettype)
        if type=="Gas Giant":
            size=np.random.choice(gasgiantsize)
        else:
            size=np.random.choice(planetsize)
        orbit=baseorbit+(10*x)
        orbitrow.append(type)
        orbitrow.append(planetcolor[type])
        orbitrow.append(size)
        orbitrow.append(planetdisplaysize[size])
        orbitrow.append(orbit)
        orbitrow.append(x)
        orbitrow.append(10)
        systemdf.loc[len(systemdf)]=orbitrow

    systemdf=systemdf[systemdf["type"]!="None"]
    asteroiddf=systemdf[systemdf["type"]=="Asteroid"]
    print(f"Star: {star}")
    print(asteroiddf)
    systemdf=systemdf[systemdf["type"]!="Asteroid"]
    print(systemdf)
    systemdf["startype"]=star

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=[0],y=[10],mode='markers',marker=dict(size=starsize+10,color='black',line=dict(color=starcolor,width=2))))
    fig.add_trace(go.Scatter(x=[0],y=[10],mode='markers',marker=dict(size=starsize,color=starcolor)))

    orbitalpaths=[]

    for index,orbitpos in systemdf.iterrows():
        print(orbitpos["orbit"])
        #fig.add_trace(go.Scatter(x=[0],y=[10],mode='markers',marker=dict(size=525+(orbitpos["orbitposition"]*349),color="rgba(0,0,0,0)",line=dict(color='white',width=0.25))))
        orbitalpaths.append(dict(type="path", path=ellipse_arc(y_center=10,a=orbitpos["orbit"],b=orbitpos["orbit"]-5,N=60),line_color="white",line_width=0.25,line_dash="dot"))


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
    return fig,systemdf

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

# Set app title

st.title("Galactic Cartographers: System View")

systemdf=pd.DataFrame()
fig,systemdf=generate_system()
with st.sidebar:
    st.image("https://i.imgur.com/PCS1XPq.png")
    if(st.button("Retrieve New System")):
        fig,systemdf=generate_system()
    st.write("Welcome to the Department of Galactic Cartography, an online catalog of nearly limitless worlds, surveyed or not.")
    st.write("-------------------------------")
    st.write("This was written to build out entire star systems for a Savage Worlds game, but with the idea of it being 100% system agnostic.")
    st.write("Scroll down to see a list of the worlds and their ID.") 
    st.write("Be sure to set them to full screen before you capture the system.")


config_globe = {'displayModeBar': True,
        'use_container_width':False}

st.plotly_chart(fig,config=config_globe)
st.dataframe(systemdf)

st.download_button(
  label="Download Planetary Records",
  data=convert_df_to_csv(systemdf),
  file_name='system.csv',
  mime='text/csv',
)

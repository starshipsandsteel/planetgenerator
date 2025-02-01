## Planet Generator

import random
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from noise import snoise3

def newplanet():
    planettype=["Desert","Jungle","Oceanic","Volcanic","Frozen","Rocky","Crystal"]
    planetsize=["Dwarf","Small","Small","Medium","Medium","Medium","Large","Giant","Gas Giant Moon"]
    planetfeatures=["Massive Canyon System","Towering Spires","Unique Weather Phenomenon","Orbital Ring","Massive Sinkholes","Titanic Geysers",
                    "Craters","Colossal Fossils", "Hostile Life: Flora","Hostile Life: Fauna"]
    planetmood=["Vibrant and Lush","Dark and Gritty","Mysterious and Eerie","Ancient and Weathered","Pristine and Serene"]
    planetsettlements=["None","Sparse","Scattered","Dense"]
    planetsettlmentsize=["Outposts","Colony","Towns","Cities","Metropolis"]
    planetdevelopment=["Low","Low","Medium","Medium","High"]
    pricemodifier=[1,1,1,1,1.25,1.25,1.5,1.5,1.75,1.75,2]
    planetarylaw=["Low","Medium","High","Martial","Military"]
    planetdistance=["Close","Medium","Far","Extreme"]
    planetatmospheretype=["Normal","Toxic storms","Acidic rains"]
    planetatmosphere=["Yes","No"]
    atmobreathable=["Normal","Toxic Clouds, partially breathable","Toxic"]
    planeticecaps=["None","Small","Large"]
    planet_prefixes = [
        "Zor", "Kry", "Xan", "Vel", "Qua", 
        "Tel", "Myr", "Gal", "Ar", "Kor", 
        "Ax", "Fen", "Nar", "Pro", "Zar", 
        "Del", "Vir", "Eon", "Ul", "Oth"
    ]
    planet_root_words = [
        "Thar", "Lon", "Xen", "Phor", "Trios", 
        "Altis", "Varn", "Solis", "Nox", "Tera", 
        "Malos", "Luma", "Vorax", "Drax", "Aurion", 
        "Zetra", "Pyra", "Vexis", "Jorun", "Osca",
        "Zyn", "Orin", "Quor", "Lira", "Thalos", 
        "Vexar", "Nyxis", "Krad", "Ophi", "Seron", 
        "Drava", "Polus", "Kyra", "Xerath", "Tarin", 
        "Malthor", "Zephy", "Arkon", "Lyros", "Cindral"
    ]
    planet_suffixes = [
        "on", "is", "ar", "ix", "us", 
        "ia", "or", "ul", "an", "eus", 
        "en", "ax"
    ]
    planet_numbers_designations = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
        "A", "B", "C", "D", "E", "X", "Y", "Z", "Alpha", "Beta", 
        "Gamma", "Delta", "Epsilon", "Prime", "Omega", "Sigma", "Kappa", "Rho", "Phi", "Tau"
    ]

    tempmodifier={"Close":10,"Medium":0,"Far":-10,"Extreme":-20}
    typetempmodifier={"Desert":20,"Jungle":20,"Oceanic":0,"Volcanic":10,"Frozen":-50,"Rocky":0,"Crystal":0,"Earth-like":0}
    basetemp={"Desert":20,"Jungle":20,"Oceanic":15,"Volcanic":10,"Frozen":-10,"Rocky":0,"Gas Giant w/ Moons":0,"Crystal":0,"Earth-like":20}
    gravitymod={"Dwarf":0.75,"Small":0.85,"Medium":1,"Large":1.3,"Giant":2,"Gas Giant Moon":0.75}
    daymod={"Dwarf":-5,"Small":-3,"Medium":0,"Large":2,"Giant":4,"Gas Giant Moon":0}

    type=random.choice(planettype)
    size=random.choice(planetsize)
    numfeat=random.randint(1,4)
    features=random.sample(planetfeatures,numfeat)
    featurelist=", ".join(features)
    mood=random.choice(planetmood)
    icecaps=random.choice(planeticecaps)

    settlements=random.choice(planetsettlements)
    if settlements!="None":
        settlementsize=random.choice(planetsettlmentsize)
        law=random.choice(planetarylaw)
        development=random.choice(planetdevelopment)
        price=random.choice(pricemodifier)
    else:    
        settlementsize="N/A"
        law="N/A"
        development="N/A"
        price="N/A"

    if planetatmosphere=="Yes":
        atmosphere=random.choice(planetatmospheretype)
        breathable=random.choice(atmobreathable)
    else:
        atmosphere="None"
        atmobreathable="No"

    distance=random.choice(planetdistance)

    temp=random.randint(10,30)+tempmodifier[distance]+basetemp[type]+typetempmodifier[type]
    gravity=round((random.randint(8,12))/10*gravitymod[size],1)
    hoursinday=random.randint(10,50)+daymod[size]

    planetnameswitch=random.randint(0,4)
    prefix=random.choice(planet_prefixes)
    root=random.choice(planet_root_words)
    suffix=random.choice(planet_suffixes)
    designation=random.choice(planet_numbers_designations)


    if planetnameswitch==0:
        planetname=prefix+root
    elif planetnameswitch==1:
        planetname=prefix+root+suffix
    elif planetnameswitch==2:
        planetname=root
    elif planetnameswitch==3:
        planetname=root+"-"+designation
    elif planetnameswitch==4:
        planetname=prefix+root+"-"+designation

    planet_dict={"name":planetname.title(),
                "type":type,
                "size":size,
                "features":featurelist,
                "icecaps":icecaps,
                "settlement size":settlementsize,
                "settlements":settlements,
                "development":development,
                "law":law,
                "Price modifier":price,
                "distance to star":distance,
                "Avg temperature (c)":temp,
                "atmosphere":atmosphere,
                "breathability":atmobreathable,
                "gravity":gravity,
                "hours in day":hoursinday}
    return planet_dict

def planet_graphics(type):
    # Parameters for random world generation
    resolution = 300            # Higher resolution for smoothness
    radius = 2.0                # Radius of the sphere
    scale = 3.0                 # Controls continent size
    octaves = 4                 # Detail level
    persistence = 0.4           # Smooth terrain transitions
    lacunarity = 2              # Frequency

    # Set random seed for reproducibility
    #np.random.seed(np.random.randint(0, 1000))
    np.random.seed(None)

    # Generate spherical coordinates
    theta = np.linspace(0, 2 * np.pi, resolution)
    phi = np.linspace(0, np.pi, resolution)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    # Convert spherical coordinates to Cartesian
    x = radius * np.sin(phi_grid) * np.cos(theta_grid)
    y = radius * np.sin(phi_grid) * np.sin(theta_grid)
    z = radius * np.cos(phi_grid)

    # Apply Simplex noise for elevation
    def generate_elevation(x, y, z):
        elevation = np.zeros_like(x)
        for i in range(resolution):
            for j in range(resolution):
                nx = x[i, j] * scale
                ny = y[i, j] * scale
                nz = z[i, j] * scale
                elevation[i, j] = snoise3(
                    nx, ny, nz,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity
                )
        return elevation

    # Generate elevation data
    elevation = generate_elevation(x, y, z)
    normalized_elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    # Apply elevation to create mountains and valleys
    x_distorted = x * (1 + 0.1 * normalized_elevation/5)
    y_distorted = y * (1 + 0.1 * normalized_elevation/5)
    z_distorted = z * (1 + 0.1 * normalized_elevation/5)

    # Color scale for terrain
    #planettype=["Desert","Jungle","Oceanic","Volcanic","Frozen","Rocky","Crystal"]
    colortype={"Desert":[[0.0,'cyan'],[0.3,"brown"],[0.5,"#391000"],[0.8,"#311308"],[1,"white"]],
               "Jungle":[[0.0, 'blue'],[0.4, 'cyan'], [0.5, 'green'], [0.7, 'brown'], [1.0, 'white']],
               "Volcanic":[[0.0, '#2D0000'],[0.4, '#501212'], [0.5, '#76441f'], [0.7, 'brown'], [1.0, 'black']],
               "Oceanic":[[0.0, 'blue'],[0.5, 'cyan'], [0.6, 'green'], [0.7, 'darkgreen'], [1.0, 'white']],
               "Frozen":[[0.0, 'cyan'],[0.4, '#B4ECFF'], [0.5, '#C7E9F5'], [0.7, '#FFFFFF'], [1.0, 'white']],
               "Rocky":[[0.0, 'cyan'],[0.4, '#674606'], [0.5, '#3F2B05'], [0.7, 'brown'], [1.0, 'white']],
               "Crystal":[[0.0, '#C54F9E'],[0.4, '#BF3893'], [0.5, '#6B2E57'], [0.7, '#CECB24'], [1.0, '#F9F401']],
               }
    colorscale=colortype[type]
    colorscale3 = [
        [0.0, 'blue'],    # Deep water
        [0.4, 'cyan'],    # Shallow water
        [0.5, 'green'],   # Lowlands
        [0.7, 'brown'],   # Mountains
        [1.0, 'white']    # Snowcaps
    ]
    colorscale2 = [
        [0.0, '#2D0000'],    # Deep water
        [0.4, '#501212'],    # Shallow water
        [0.5, '#76441f'],   # Lowlands
        [0.7, 'brown'],   # Mountains
        [1.0, 'black']    # Snowcaps
    ]

    # Create the globe plot
    fig = go.Figure(data=[
        go.Surface(
            x=x_distorted,
            y=y_distorted,
            z=z_distorted,
            surfacecolor=normalized_elevation,
            colorscale=colorscale,
            cmin=0,
            cmax=1,
            showscale=False,
            opacity=1.0
        )
    ])
    fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        aspectmode='data',
        bgcolor='black'
        )
    )
    return fig


st.title("Planet Generator")
planet_dict=newplanet()
planet_fig=planet_graphics(planet_dict["type"])
col1, col2 = st.columns(2)
for x in planet_dict:
    col1.write (f"{x.title()}: {planet_dict[x]}")


col2.plotly_chart(planet_fig,use_container_width=False)
with st.sidebar:
    st.image("https://i.imgur.com/PCS1XPq.png")
    if(st.button("Generate New World")):
        planet_dict=newplanet()

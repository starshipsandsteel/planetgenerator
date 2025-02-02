## Planet Generator

import random
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from noise import snoise3

def newplanet():
    planettype=["Desert","Jungle","Oceanic","Volcanic","Frozen","Rocky","Crystal"]
    planetsize=["Dwarf","Small","Small","Medium","Medium","Medium","Large","Giant","Gas Giant Moon"]
    planetfeatures=["Massive Canyon System","Towering Spires","Unique Weather Phenomenon","Massive Sinkholes","Titanic Geysers",
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
    planeticecaps=["None","Small","Medium","Large"]
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

def planet_graphics(type,caps):
    # Parameters for random world generation
    resolution = 400            # Higher resolution for smoothness
    radius = 1.0                # Radius of the sphere
    base_scale = 2.0            # Base scale for continent size
    octaves = 5                 # Detail level
    persistence = 0.6           # Smooth terrain transitions
    lacunarity = 2.0            # Frequency

    # Randomize parameters for unique worlds
    np.random.seed()  # Ensures randomness on each run
    random_offset = np.random.uniform(-1000, 1000, size=3)  # Random offset for noise
    scale_variation = np.random.uniform(0.8, 1.2)           # Random variation in scale
    scale = base_scale * scale_variation

    # Generate spherical coordinates
    theta = np.linspace(0, 2 * np.pi, resolution)
    phi = np.linspace(0, np.pi, resolution)
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    # Convert spherical coordinates to Cartesian
    x = radius * np.sin(phi_grid) * np.cos(theta_grid)
    y = radius * np.sin(phi_grid) * np.sin(theta_grid)
    z = radius * np.cos(phi_grid)

    # Apply Simplex noise for elevation
    def generate_elevation(x, y, z, offset):
        elevation = np.zeros_like(x)
        for i in range(resolution):
            for j in range(resolution):
                nx = (x[i, j] + offset[0]) * scale
                ny = (y[i, j] + offset[1]) * scale
                nz = (z[i, j] + offset[2]) * scale
                elevation[i, j] = snoise3(
                    nx, ny, nz,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity
                )
        return elevation

    # Generate elevation data
    elevation = generate_elevation(x, y, z, random_offset)
    normalized_elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    # Apply elevation to create mountains and valleys
    x_distorted = x * (1 + 0.1 * normalized_elevation/5)
    y_distorted = y * (1 + 0.1 * normalized_elevation/5)
    z_distorted = z * (1 + 0.1 * normalized_elevation/5)

    # Generate Perlin noise for natural ice cap edges
    ice_noise = np.zeros_like(x)
    for i in range(resolution):
        for j in range(resolution):
            ice_noise[i, j] = snoise3(
                i / 50.0, j / 50.0, random_offset[0],
                octaves=2, persistence=0.5, lacunarity=2.0
            )
    # ice dictionary
    icethresh={"None":90,"Small":80,"Medium":70,"Large":65}
    ice=icethresh[caps]

    # Ice cap mask with smooth, noisy edges
    latitude = 90 - np.degrees(phi_grid)      # Latitude from -90 to 90
    ice_threshold = ice                 # Base latitude for ice caps

    # Apply noise and create a smooth gradient using a sigmoid function
    dice_transition = (np.abs(latitude) + (ice_noise * 5) - ice_threshold) / 5  # Smoother transition
    ice_cap_gradient = 1 / (1 + np.exp(-dice_transition))                      # Sigmoid smoothing

    # Blend ice cap gradient with terrain
    combined_terrain = np.maximum(normalized_elevation, ice_cap_gradient)

    # Color scale for terrain
    #planettype=["Desert","Jungle","Oceanic","Volcanic","Frozen","Rocky","Crystal"]
    colortype={"Desert":[[0.0,'cyan'],[0.3,"#eacf4c"],[0.5,"#d4b623"],[0.8,"#b79c18"],[0.9,"white"],[1,"#E0FFFF"]],
               "Jungle":[[0.0, 'blue'],[0.4, 'cyan'], [0.5, 'green'], [0.7, 'brown'], [0.9, 'white'],[1,"#E0FFFF"]],
               "Volcanic":[[0.0, '#2D0000'],[0.4, '#501212'], [0.5, '#76441f'], [0.7, 'brown'], [0.9, 'black'],[1,"#E0FFFF"]],
               "Oceanic":[[0.0, 'blue'],[0.5, 'cyan'], [0.6, 'green'], [0.7, 'darkgreen'], [0.9, 'white'],[1,"#E0FFFF"]],
               "Frozen":[[0.0, 'cyan'],[0.4, '#B4ECFF'], [0.5, '#C7E9F5'], [0.7, '#FFFFFF'], [0.9, 'white'],[1,"#E0FFFF"]],
               "Rocky":[[0.0, 'cyan'],[0.4, '#674606'], [0.5, '#3F2B05'], [0.7, 'brown'], [0.9, 'white'],[1,"#E0FFFF"]],
               "Crystal":[[0.0, '#C54F9E'],[0.4, '#BF3893'], [0.5, '#6B2E57'], [0.7, '#CECB24'], [0.9, 'white'],[1,"#E0FFFF"]],
               }
    colorscale=colortype[type]

    # Create the globe plot
    fig = go.Figure(data=[
        go.Surface(
            x=x_distorted,
            y=y_distorted,
            z=z_distorted,
            surfacecolor=combined_terrain,
            colorscale=colorscale,
            cmin=0,
            cmax=1,
            showscale=False,
            opacity=1.0
        )
    ])

    fig.update_layout(
    autosize=False,
    width=800,
    height=700,
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        aspectmode='data',
        bgcolor='black'
        )
    )

    # === Flat 2:1 Map Projection ===
    longitude = np.degrees(theta_grid) - 180  # Longitude from -180 to 180
    latitude = 90 - np.degrees(phi_grid)      # Latitude from -90 to 90

    fig_flat = go.Figure(data=[
        go.Heatmap(
            z=combined_terrain,
            x=longitude[0],
            y=latitude[:, 0],
            colorscale=colorscale,
            zmin=0,
            zmax=1,
            showscale=False
        )
    ])

    fig_flat.update_layout(
        #title='Flat Map Projection (Equirectangular)',
        #xaxis=dict(title='Longitude', showgrid=False, zeroline=False),
        #yaxis=dict(title='Latitude', showgrid=False, zeroline=False),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='black',
        width=1800,
    )
    return fig,fig_flat


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
    </style>
    """, unsafe_allow_html=True
)
st.title("Planet Generator")
col1, col2 = st.columns(2,vertical_alignment="top",border=True)
planet_dict=newplanet()
planet_fig,planet_map=planet_graphics(planet_dict["type"],planet_dict["icecaps"])

config_globe = {'displayModeBar': True,
          'use_container_width':False}

col2.plotly_chart(planet_fig,config=config_globe)
st.plotly_chart(planet_map)
for x in planet_dict:
    col1.write (f"{x.title()}: {planet_dict[x]}")

with st.sidebar:
    st.image("https://i.imgur.com/PCS1XPq.png")
    if(st.button("Generate New World")):
        planet_dict=newplanet()

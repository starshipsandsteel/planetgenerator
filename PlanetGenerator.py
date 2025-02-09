## Planet Generator

import random
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from noise import snoise3

def newplanet(selectedtype,selectedsize):
    planettype=["Desert","Jungle","Oceanic","Volcanic","Frozen","Rocky","Crystal","Steppe"]
    planetsize=["Dwarf","Small","Small","Medium","Medium","Medium","Large","Giant","Gas Giant Moon"]
    planetfeatures=["Massive Canyon System","Towering Spires","Unique Weather Phenomenon","Massive Sinkholes","Titanic Geysers",
                    "Craters","Colossal Fossils", "Hostile Life: Flora","Hostile Life: Fauna"]
    #planetmood=["Vibrant and Lush","Dark and Gritty","Mysterious and Eerie","Ancient and Weathered","Pristine and Serene"]
    planetsettlements=["None","Sparse","Scattered","Dense"]
    planetsettlmentsize=["Outposts","Colony","Towns","Cities","Metropolis"]
    planetdevelopment=["Low","Low","Medium","Medium","High"]
    pricemodifier=[1,1,1,1,1.25,1.25,1.5,1.5,1.75,1.75,2]
    planetarylaw=["Low","Medium","High","Martial","Military"]
    planetdistance=["Close","Medium","Far","Extreme"]
    planetatmospheretype=["Normal","Thin","Trace","Thick"]
    planetatmosphere=["Yes","No"]
    atmobreathable=["Breathable","Breathable","Breathable","Toxic Clouds","Acid Rain"]
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
    typetempmodifier={"Desert":20,"Jungle":20,"Oceanic":0,"Volcanic":10,"Frozen":-50,"Rocky":0,"Crystal":0,"Steppe":0}
    basetemp={"Desert":20,"Jungle":20,"Oceanic":15,"Volcanic":10,"Frozen":-10,"Rocky":0,"Gas Giant w/ Moons":0,"Crystal":0,"Steppe":20}
    gravitymod={"Dwarf":0.75,"Small":0.85,"Medium":1,"Large":1.3,"Giant":2,"Gas Giant Moon":0.75}
    daymod={"Dwarf":-5,"Small":-3,"Medium":0,"Large":2,"Giant":4,"Gas Giant Moon":0}

    if selectedtype=="Any":
        type=random.choice(planettype)
    else:
        type=selectedtype
    if selectedsize=="Any":
        size=random.choice(planetsize)
    else:
        size=selectedsize
    numfeat=random.randint(1,4)
    features=random.sample(planetfeatures,numfeat)
    featurelist=", ".join(features)
    #mood=random.choice(planetmood)
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

    planetatmochoice=random.choice(planetatmosphere)   
    if type=="Oceanic" or type=="Jungle":
        planetatmochoice="Yes"
    if planetatmochoice=="Yes":
        atmosphere=random.choice(planetatmospheretype)
        breathable=random.choice(atmobreathable)
    else:
        atmosphere="None"
        breathable="None"

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
                "atmosphere notes":breathable,
                "gravity":gravity,
                "hours in day":hoursinday}
    return planet_dict

def planet_graphics(type,caps,size):
    
    psize={"Dwarf":0.75,"Small":1,"Medium":1.25,"Large":1.75,"Giant":2,"Gas Giant Moon":0.70}
    psizeres={"Dwarf":200,"Small":250,"Medium":300,"Large":450,"Giant":500,"Gas Giant Moon":200}
    size_attrib=psize[size]
    sizeres=psizeres[size]
    # Parameters for random world generation
    resolution = int(sizeres)       # Higher resolution for smoothness
    radius = size_attrib            # Radius of the sphere
    base_scale = size_attrib*1.5    # Base scale for continent size
    octaves = 5                     # Detail level
    persistence = 0.6               # Smooth terrain transitions
    lacunarity = 2.0                # Frequency

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
    icethresh={"None":90,"Small":75,"Medium":65,"Large":60}
    ice=icethresh[caps]

    # Ice cap mask with smooth, noisy edges
    latitude = 90 - np.degrees(phi_grid)      # Latitude from -90 to 90
    ice_threshold = ice                 # Base latitude for ice caps

    # Apply noise and create a smooth gradient using a sigmoid function
    dice_transition = (np.abs(latitude) + (ice_noise * 2) - ice_threshold) / 5  # Smoother transition
    ice_cap_gradient = 1 / (1 + np.exp(-dice_transition))                      # Sigmoid smoothing

    # Blend ice cap gradient with terrain
    combined_terrain = np.maximum(normalized_elevation, ice_cap_gradient)

    # get POI range per type
    poirange={"Oceanic":[0.8,.9],"Desert":[0.1,.9],"Volcanic":[0.6,.9],"Frozen":[0.1,.9],"Rocky":[0,.9],"Crystal":[0,.9],"Jungle":[0.4,.9],"Steppe":[0.4,.9]}
    lower=poirange[type][0]
    upper=poirange[type][1]
    # Add Points of Interest (POIs)
    poi_indices = np.argwhere((combined_terrain > lower) & (combined_terrain< upper))
    rng = np.random.default_rng()
    poinumber=rng.integers(5)+1
    selected_pois = poi_indices[np.random.choice(poi_indices.shape[0], size=poinumber, replace=False)]  # Select 5 random POIs
    textpoints=[]
    for x in range(1,poinumber+1):
        textpoints.append(str(x))

    # Extract coordinates for POIs
    #poi_x = x_distorted[selected_pois[:, 0], selected_pois[:, 1]]
    #poi_y = y_distorted[selected_pois[:, 0], selected_pois[:, 1]]
    #poi_z = z_distorted[selected_pois[:, 0], selected_pois[:, 1]]
    poi_lat = latitude[selected_pois[:, 0], selected_pois[:, 1]]
    poi_lon = np.degrees(theta_grid[selected_pois[:, 0], selected_pois[:, 1]]) - 180

    # Color scale for terrain
    colortype={"Desert":[[0.0,'cyan'],[0.1,"#c4830d"],[0.5,"#aa6d04"],[0.7,"#835204"],[0.95,"#643c04"],[1,"#E0FFFF"]],
               "Jungle":[[0.0, 'blue'],[0.3, 'cyan'], [0.4, 'green'], [0.7, 'darkgreen'],[0.8, 'saddlebrown'], [0.95, 'white'],[1,"#E0FFFF"]],
               "Volcanic":[[0.0, '#ff0800'],[0.2, '#560319'],[0.3, '#65000b '], [0.35, '#a81c07'], [0.6, '#321414'],[0.7, 'brown'], [0.95, 'black'],[1,"#E0FFFF"]],
               "Oceanic":[[0.0, 'navy'],[0.5, 'blue'],[0.6, '#3c99dc'], [0.75, 'cyan'], [0.8, 'green'], [0.95, 'white'],[1,"#E0FFFF"]],
               "Frozen":[[0.0, 'cyan'],[0.4, '#B4ECFF'], [0.5, '#C7E9F5'], [0.5, '#eab676'], [0.65, '#FFFFFF'], [0.9, 'white'],[1,"#E0FFFF"]],
               "Rocky":[[0.0, '#483104'],[0.4, '#674606'], [0.5, '#3F2B05'], [0.85, '#865b0b '], [0.98, 'white'],[1,"#E0FFFF"]],
               "Crystal":[[0.0, '#C54F9E'],[0.4, '#BF3893'], [0.5, '#6B2E57'], [0.7, '#CECB24'], [0.95, 'white'],[1,"#E0FFFF"]],
               "Steppe":[[0.0, 'blue'],[0.2, 'cyan'], [0.35, '#fff59d'], [0.5, '#dce775'],[0.6, '#8bc34a'],[0.7, '#f3bc77'],[0.9, '#402a23'], [0.95, 'white'],[1,"#E0FFFF"]],
               }
    colorscale=colortype[type]
    if type=="Volcanic":
        dotcolor="black"
    else:
        dotcolor="red"

    # Create the globe plot
    fig = go.Figure(data=[
        go.Surface(
            x=x_distorted,
            y=y_distorted,
            z=z_distorted,
            surfacecolor=combined_terrain,
            colorscale=colorscale,
            cmin=0,
            cmax=1,  # Adjusted to fit color range
            showscale=False,
            opacity=1.0
        )
    ])

    fig.update_layout(
    autosize=False,
    width=800,
    height=700,
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
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

    fig_flat_poi = go.Figure(data=[
        go.Heatmap(
            z=combined_terrain,
            x=longitude[0],
            y=latitude[:, 0],
            colorscale=colorscale,
            zmin=0,
            zmax=1,
            showscale=False
        ),
        go.Scatter(
            x=poi_lon,
            y=poi_lat,
            mode='markers+text',
            text=textpoints,
            marker=dict(size=20, color=dotcolor, symbol='octagon'),
            name='Points of Interest'
        )
    ])
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

    fig_flat_poi.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        template='plotly_dark',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='black',
        width=1800
    )
    fig_flat.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        template='plotly_dark',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='black',
        width=1800
    )

    return fig,fig_flat_poi,fig_flat,poinumber

# Random name generator for POIs
def generate_poi_name(poi_type):
    natural_prefixes = ["Whispering", "Emerald", "Silent", "Crimson", "Frozen", "Golden"]
    natural_suffixes = [
        "Forest", "Lake", "Cliffs", "Canyon", "Springs", "Glade",
        "Meadow", "Valley", "Ridge", "Grove", "Bay", "Marsh", "Dunes", "Plateau"
    ]

    manmade_prefixes = ["Ancient", "Lost", "Mystic", "Hidden", "Crystal", "Dark"]
    manmade_suffixes = [
        "Fortress", "Ruins", "Citadel", "Temple", "Outpost", "Sanctuary",
        "Tower", "Keep", "Bastion", "Monastery", "Stronghold", "Observatory", "Vault", "Shrine"
    ]

    if poi_type == "Natural":
        return f"{random.choice(natural_prefixes)} {random.choice(natural_suffixes)}"
    else:
        return f"{random.choice(manmade_prefixes)} {random.choice(manmade_suffixes)}"

# Generate Points of Interest (POIs)
def generate_pois(num_pois):
    # Create POI data with types
    poi_types = ["Natural", "Man-made"]
    pois = []
    for x in range(0,num_pois):
        poi_type = random.choice(poi_types)
        name = generate_poi_name(poi_type)
        pois.append({
            "name": name,
            "type": poi_type
        })

    return pois

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
    planet_dict=newplanet("Any","Any")
    planet_fig,planet_map_poi,planet_map,pois=planet_graphics(planet_dict["type"],planet_dict["icecaps"],planet_dict["size"])
    poidict=generate_pois(pois)

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



with st.sidebar:
    st.image("https://i.imgur.com/PCS1XPq.png")
    planettype=st.selectbox("Planet Type to Retrieve",("Any","Desert","Jungle","Rocky","Crystal","Frozen","Volcanic","Steppe"),)
    planetsize=st.selectbox("Planet Size to Retrieve",("Any","Gas Giant Moon","Dwarf","Small","Medium","Large","Giant"),)
    if(st.button("Retrieve New World")):
        planet_dict=newplanet(planettype,planetsize)
        planet_fig,planet_map_poi,planet_map,pois=planet_graphics(planet_dict["type"],planet_dict["icecaps"],planet_dict["size"])
        poidict=generate_pois(pois)
        st.session_state["poimap"]=planet_map_poi
        st.session_state["map"]=planet_map
        st.session_state["planet_fig"]=planet_fig
        st.session_state["planet_dict"]=planet_dict
        st.session_state["planet_poi"]=poidict
        print(st.session_state["planet_dict"]["name"])
    poi_onoff=st.toggle("Show POIs")

    st.write("Welcome to the Department of Galactic Cartography, an online catalog of nearly limitless worlds, surveyed or not.")
    st.write("-------------------------------")
    st.write("This was written to create planets for a Savage Worlds game, but with the idea of it being 100% system agnostic.")
    st.write("Scroll down to see a map view of the world, and you can use the image controls to save images of the planet globe and map.") 
    st.write("Be sure to set them to full screen before you capture them, especially the map.")
    st.write("Below the planetary map, is a second map displaying planetary sites to be explored.")
    #st.write("-------------------------------")
    #st.image("https://i.imgur.com/kv7vuDb.png")

print("Update title")
st.header(st.session_state['planet_dict']['name'])

config_globe = {'displayModeBar': True,
        'use_container_width':False}

col1, col2 = st.columns(2,vertical_alignment="top",border=True)

for x in st.session_state["planet_dict"]:
    if x!="name":
        col1.write (f"{x.title()}: {st.session_state['planet_dict'][x]}")
col2.plotly_chart(st.session_state["planet_fig"],config=config_globe)
st.header('Planetary Map View')
if poi_onoff:
    st.plotly_chart(st.session_state["poimap"])
else:
    st.plotly_chart(st.session_state["map"])
#st.header('Planetary Sites View')

st.write("Planetary Sites")
for x in range(0,len(st.session_state["planet_poi"])):
    st.write(f"{x+1}: {st.session_state['planet_poi'][x]['name']} ({st.session_state['planet_poi'][x]['type']})")





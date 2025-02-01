## Planet Generator

import random
import json
import streamlit as st

def newplanet():
    planettype=["Desert","Jungle","Oceanic","Volcanic","Frozen","Rocky","Crystal"]
    planetsize=["Dwarf","Small","Small","Medium","Medium","Medium","Large","Giant","Gas Giant Moon"]
    planetfeatures=["Massive Canyon System","Towering Spires","Unique Weather Phenomenon","Orbital Ring","Massive Sinkholes","Titanic Geysers",
                    "Craters","Colossal Fossils", "Hostile Life: Flora","Hostile Life: Fauna"]
    planetmood=["Vibrant and Lush","Dark and Gritty","Mysterious and Eerie","Ancient and Weathered","Pristine and Serene"]
    planetsettlements=["None","Sparse","Scattered","Dense"]
    planetsettlmentsize=["Outposts","Colony","Towns","Cities","Metropolis"]
    planetdevelopment=["1","1","2","2","2"]
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
    featurelist=",".join(features)
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
                "temperature":temp,
                "atmosphere":atmosphere,
                "breathability":atmobreathable,
                "gravity":gravity,
                "hours in day":hoursinday}
    return planet_dict

st.title("Planet Generator")
planet_dict=newplanet()
col1, col2 = st.columns(2)
for x in planet_dict:
    col1.write (f"{x.title()}: {planet_dict[x]}")
#planetfile=r"D:\00_Projects\2025 Campaign - 2nd Saturday\Sci-Fi 2025\Planetary Images and Maps\planets.json"
if(st.button("Generate New World")):
    planet_dict=newplanet()
'''
with open(planetfile,'a',encoding='utf-8') as outfile:
    json.dump(planet_dict,outfile)
'''
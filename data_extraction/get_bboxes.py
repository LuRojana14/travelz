import pandas as pd
import numpy as np
import requests
from pathlib import Path
import json
from pymongo import MongoClient 

# myclient = pymongo.MongoClient("Aquí Incluir nuestro MONGO") #TODO
# mydb = myclient["Inlcuir nombre de la base de datos"]  #TODO
# mysearch = mydb["nombre de la colección a traernos"]   #TODO
# city_info = mysearch.find(Incluimos la query que necesitemos)  #TODO

city_info = [{    #Sustituiremos esto por la llamada al MONGO 

    "name": "Madrid", 

    "country": "ES", 

    "lat": 40.4165, 

    "lon": -3.70256, 

    "population": 3255944, 

    "timezone": "Europe/Madrid", 

    "status": "OK" 

}, 

{ 

    "name": "Barcelona", 

    "country": "ES", 

    "lat": 41.38879, 

    "lon": 2.15899, 

    "population": 1621537, 

    "timezone": "Europe/Madrid", 

    "status": "OK" 

}] 

dff = pd.DataFrame()
i = 0
for item in city_info:
    item.update( {"POIS":""})

for i in range(len(city_info)):

    for key in city_info[i]:

        name = city_info[i]["name"]
        country = city_info[i]["country"]
        lat = float(city_info[i]["lat"])
        lon = float(city_info[i]["lon"])
        population = city_info[i]["population"]
        lat_max = lat+0.1
        lat_min = lat-0.1
        lon_max = lon+0.1
        lon_min = lon-0.1
        
        
        url = f"https://api.opentripmap.com/0.1/en/places/bbox?apikey=5ae2e3f221c38a28845f05b6a409d09f601e71c512bebd50adbc3222&lon_min={lon_min}&lon_max={lon_max}&lat_min={lat_min}&lat_max={lat_max}&limit=100"
        r = requests.get(url)
        POIS = r.json()
        city_info[i].update({'POIS':POIS})


#para comporbar en excel que datos tenemos en la colección
    dfi = pd.DataFrame(np.array([[name, country, lat,lon,population,lat_max,lat_min,lon_max,lon_min,POIS]]),columns=['name', 'country', 'lat', 'lon','population','lat_max','lat_min','lon_max','lon_min','POIS'])
    dff = dff.append(dfi)        

filepath = Path('C:\\Users/34649/OneDrive/Escritorio/Proyecto_final/out.xls')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
dff.to_excel(filepath)  


# Crear colección en MONGO e insertar la info #TODO
# mycol = mydb["city_info"]
# 
# insert_db = mycol.insert_one(city_info)"]




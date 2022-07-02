import pandas as pd
import numpy as np
import pymongo
import requests
from pymongo import MongoClient


myclient = pymongo.MongoClient(host="localhost", port=27017) # Poner el mongo del proyecto TODO
mydb = myclient["Prueba_concepto_travelz"]  #Poner la BBDD del proyecto TODO


city_info = [{   # de esta linea a la 52 irá fuera (son mis pruebas locales)

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



mycol = mydb["city_info"] 
x = mycol.insert_many(city_info)  #prueba de concepto creando la colección antes de llamar


mycol = mydb["city_info"]  # incluir nombre de la colleción de la bbdd del proyecto

x = mycol.find()
city_info = list(x)  #TODO


for i in range(len(city_info)):
        
        city_info_POIS = []
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
        POIS["City_Name"] = name
        i=0
        for key in POIS["features"]:
            POIS["features"][i]["properties"]["kinds"] = POIS["features"][i]["properties"]["kinds"].replace("_"," ")
            POIS["features"][i]["properties"]["kinds"] = POIS["features"][i]["properties"]["kinds"].split(",")
            i+=1
        city_info_POIS = POIS
        mycol_2 = mydb["city_info_POIS"]
        insert_db_2 = mycol_2.insert_one(city_info_POIS)
            






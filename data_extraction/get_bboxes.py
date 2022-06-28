import pandas as pd
import numpy as np
import pymongo
import requests
from pymongo import MongoClient


myclient = pymongo.MongoClient(host="localhost", port=27017) #TODO
mydb = myclient["Prueba_concepto_travelz"]  #TODO


city_info = [{

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
 #prueba de concepto creando la colección antes de llamar
x = mycol.insert_many(city_info)
mycol = mydb["city_info"] 

x = mycol.find()
city_info = list(x)  #TODO


# city_info = mysearch.find(Incluimos la query que necesitemos en caso de necesitarla)  #TODO


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
        #city_info_POIS[i].update({'POIS':POIS})
        city_info_POIS = POIS

# del city_info_POIS[i]['_id']

# Crear colección en MONGO e insertar la info #TODO
mycol_2 = mydb["city_info_POIS"]

insert_db_2 = mycol_2.insert_one(city_info_POIS)




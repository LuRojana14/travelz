import pandas as pd
import numpy as np
import pymongo
import requests
from pymongo import MongoClient
from tqdm import tqdm
import time

username = "grupoData"
password = "danilumar"
url_mongo = f"mongodb+srv://{username}:{password}@cluster0.kaxbhpi.mongodb.net/?retryWrites=true&w=majority"
myclient = MongoClient(url_mongo)
mydb = myclient["Proyecto"]
mycol = mydb["ciudades"]  # incluir nombre de la colleción de la bbdd del proyecto


apikey = "5ae2e3f221c38a28845f05b6016da788551ff5bd63dd000135198a44"


x = mycol.find()
city_info = list(x)

for i in tqdm(range(len(city_info))):

    city_info_POIS = []
    name = city_info[i]["name"]
    country = city_info[i]["country"]
    lat = float(city_info[i]["lat"])
    lon = float(city_info[i]["lon"])
    lat_max = lat + 0.1
    lat_min = lat - 0.1
    lon_max = lon + 0.1
    lon_min = lon - 0.1

    url = f"https://api.opentripmap.com/0.1/en/places/bbox?apikey={apikey}&lon_min={lon_min}&lon_max={lon_max}&lat_min={lat_min}&lat_max={lat_max}&limit=100"
    r = requests.get(url)
    POIS = r.json()
    POIS["City_Name"] = name
    i = 0
    for key in POIS["features"]:
        POIS["features"][i]["properties"]["kinds"] = POIS["features"][i]["properties"][
            "kinds"
        ].replace("_", " ")
        POIS["features"][i]["properties"]["kinds"] = POIS["features"][i]["properties"][
            "kinds"
        ].split(",")
        i += 1
    city_info_POIS = POIS
    mycol_2 = mydb["city_info_POIS"]
    insert_db_2 = mycol_2.insert_one(city_info_POIS)
    time.sleep(1)

mycol = mydb["city_info"]  # incluir nombre de la colleción de la bbdd del proyecto

x = mycol.find()
city_info = list(x)  #TODO


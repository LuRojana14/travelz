# Código de Lourdes

import pandas as pd
import requests
from pymongo import MongoClient
from tqdm import tqdm
import time


username = "grupoData"
password = "danilumar"
url_mongo = f"mongodb+srv://{username}:{password}@cluster0.kaxbhpi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url_mongo)
db = client["Proyecto"]
col = db["ciudades"]

# url_base = "https://api.opentripmap.com/0.1/en/places/geoname"
apikey = "5ae2e3f221c38a28845f05b6016da788551ff5bd63dd000135198a44"

url = f"https://api.opentripmap.com/0.1/en/places/geoname?apikey={apikey}&name="

path = r"C:\Users\maria\OneDrive\Escritorio\Proyecto_final\loc (1).csv"
df = pd.read_csv(path)

spain_cities = df["NOMBRE"]


for city in tqdm(spain_cities):
    mongo_result = list(col.find({"name": city}))
    if len(mongo_result) != 0:
        continue
    response = requests.get(url + city)
    if response.status_code == 200:
        data = response.json()
        col.insert_one(data)
    else:
        print("Error")
    time.sleep(0.5)


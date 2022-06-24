import pandas as pd
import numpy as np
import requests
from pathlib import Path
import json

city = [{    #Aqui meteremos la llamada al MONGO #TODO

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
for item in city:
    item.update( {"POIS":""})

for i in range(len(city)):

    for key in city[i]:

        name = city[i]["name"]
        country = city[i]["country"]
        lat = float(city[i]["lat"])
        lon = float(city[i]["lon"])
        population = city[i]["population"]
        lat_max = lat+0.1
        lat_min = lat-0.1
        lon_max = lon+0.1
        lon_min = lon-0.1
        
        
        url = f"https://api.opentripmap.com/0.1/en/places/bbox?apikey=5ae2e3f221c38a28845f05b6a409d09f601e71c512bebd50adbc3222&lon_min={lon_min}&lon_max={lon_max}&lat_min={lat_min}&lat_max={lat_max}&limit=100"
        r = requests.get(url)
        POIS = r.json()
        city[i].update({'POIS':POIS})



    dfi = pd.DataFrame(np.array([[name, country, lat,lon,population,lat_max,lat_min,lon_max,lon_min,POIS]]),columns=['name', 'country', 'lat', 'lon','population','lat_max','lat_min','lon_max','lon_min','POIS'])
    dff = dff.append(dfi)        

    print(dff)


# conectar a MONGO #TODO

filepath = Path('C:\\Users/34649/OneDrive/Escritorio/Proyecto_final/out.xls')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
dff.to_excel(filepath)  


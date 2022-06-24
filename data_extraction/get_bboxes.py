import pandas as pd
import numpy as np
import requests
from pathlib import Path
import json

File = "C:\\Users/34649/OneDrive/Escritorio/Proyecto_final/loc.csv"
df = pd.read_csv(File, sep=";")


i = 0
loc = ""
dff =  pd.DataFrame()
while i <= 200: #df.shape[0]:
    loc = df.iloc[[i],[0]]
    
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?apikey=5ae2e3f221c38a28845f05b6a409d09f601e71c512bebd50adbc3222&name={loc}"
    r = requests.get(url)
    r = r.json()

    if r["status"] == 'NOT_FOUND':
            i += 1
            print(r)
    else:

        name = r["name"]
        country = r["country"]
        lat = float(r["lat"])
        lon = float(r["lon"])
        lat_max = float(r["lat"])+0.1
        lat_min = float(r["lat"])-0.1
        lon_max = float(r["lon"])+0.1
        lon_min = float(r["lon"])-0.1

        dfi = pd.DataFrame(np.array([[name, country, lat,lon,lat_max,lat_min,lon_max,lon_min]]),columns=['name', 'country', 'lat', 'lon','lat_max','lat_min','lon_max','lon_min'])
        dff = dff.append(dfi)        

        i += 1
        print(dff)



filepath = Path('C:\\Users/34649/OneDrive/Escritorio/Proyecto_final/out.xls')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
dff.to_excel(filepath)  


import numpy as np 
import pymongo
from pymongo import MongoClient 
import pandas as pd
import spacy 
from sklearn.neighbors import NearestNeighbors
from bson.json_util import dumps
import json


nlp = spacy.load("es_core_news_md") 


# ============================================================================= 

# Fase 1, extraer palabras clave y localización 

# ============================================================================= 

query_user = input("¿A donde quieres ir?") # esto será el input

doc = nlp(query_user) 

spacy.displacy.render(doc) #pintar el esquema. No hace falta

for tok in doc: 

    if tok.pos_ == "NOUN":
        noun_ = str(tok)
        print(noun_)
    else:
        if tok.pos_ == "VERB":
            noun_ = str(tok)
            print(noun_)

#Matcher para buscar patrones ()

for ent in doc.ents: 

    if ent.label_ == "LOC": 
        ent_ = str(tok).capitalize()

        print(ent)  


# ============================================================================= 

# Fase 2, emparejar las características con lo más similar en nuestra bbdd 

# ============================================================================= 


#traer kinds traducidos del archivo JSON (Lourdes)   TODO


# Loop para meter vectores en el array y crear un df para ver que vector es el mejor (Ojo saltar error si no encuentra el vector)

JSON = []  #esto será el archivo JSON con las traducciones TODO
X = np.array( [ ] ) 
df_kinds = pd.DataFrame()
i=0
for i in {JSON}:
    y = np.array( [nlp("prueba").vector])  # en prueba debe coger el kind  del JSON traducido TODO
    df2_kinds = pd.DataFrame({"id_":[i],"kind":f"prueba{i}"})  # en prueba debe coger el kind  del JSON traducido TODO
    df_kinds = df_kinds.append(df2_kinds,ignore_index = True)
    X = np.append(X,y, axis=0)
    i+=1



#modelo KNN

nn = NearestNeighbors(n_neighbors=1) 

nn.fit(X) 

test_word = nlp(noun_).vector.reshape(1, -1) 

Result = list(nn.kneighbors(test_word))
Result = Result[1]
Result = Result[0]
Result = int(Result[0])


print(f"este numero es: {Result}")  #numero del array resultante como más similar (para pruebas)

#valor resultante

kind_result = df_kinds.query(f"id_ == {Result}")
kind_result= kind_result["kind"]
kind_result = dict(kind_result)
kind_result = kind_result[Result] 


# traducir al ingles los kinds results  TODO
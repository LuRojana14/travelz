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

#Matcher para buscar patrones ( relaciones nombres con obj adj y guardar varios nouns)

for ent in doc.ents: 

    if ent.label_ == "LOC": 
        ent_ = str(tok).capitalize()

        print(ent)  


# ============================================================================= 

# Fase 2, emparejar las características con lo más similar en nuestra bbdd 

# ============================================================================= 



# Loop para meter vectores en el array y crear un df para ver que vector es el mejor

url = "C:\\Users/34649/OneDrive/Escritorio/Proyecto_final/travelz/translations_enTo_es - translations.csv"  # poner url proyecto TODO
csv = pd.read_csv(url)  
X = np.array( [ nlp("").vector, ] ) 
df_kinds = pd.DataFrame()
j=0
for i in csv["spanish_words"]:

    y = np.array( [nlp(i).vector]) 
    df2_kinds = pd.DataFrame({"id_":[j],"kind":f"{i}","city":f"{ent_}"})  
    df_kinds = df_kinds.append(df2_kinds,ignore_index = True)
    X = np.append(X,y,axis =0)
    j+=1



#modelo KNN

nn = NearestNeighbors(n_neighbors=1) 

nn.fit(X) 

test_word = nlp(noun_).vector.reshape(1, -1) 

Result = list(nn.kneighbors(test_word))
Result = Result[1]
Result = Result[0]
Result = int(Result[0])


print(f"este numero es: {Result}")  #numero del array resultante como más similar (para pruebas)


kind_result = df_kinds.query(f"id_ == {Result}")
kind_result= kind_result["kind"]
kind_result = dict(kind_result)
kind_result = kind_result[Result]  # kind clave




























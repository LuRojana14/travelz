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

List_noun_ = []
for tok in doc:
    
    if tok.pos_ == "NOUN":
        noun_1 = str(tok)
        List_noun_.append(noun_1)

    else:
        if tok.pos_ == "VERB":
            noun_ = str(tok)

for ent in doc.ents: 

    if ent.label_ == "LOC": 
        ent_ = str(tok).capitalize()

List_adj_ = []
for tok in doc:
    
    if tok.pos_ == "ADJ":
        adj_1 = str(tok)
        doc_list = str(doc).split()
        index = doc_list.index(adj_1)
        noun_prev = doc_list[index-1]
        List_adj_.append(f"{noun_prev} {adj_1}")


# ============================================================================= 

# Fase 2, emparejar las características con lo más similar en nuestra bbdd 

# ============================================================================= 

# Loop para meter vectores en el array y crear un df para ver que vector es el mejor

url = "C:\\Users/34649/OneDrive/Escritorio/Proyecto_final/travelz/translations_enTo_es - translations.csv"  # poner url proyecto TODO
csv = pd.read_csv(url)  
X = np.array( [ nlp("esto es un vector de inicio").vector, ] ) 
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

List_kind_ = []
for i in  List_noun_:

    test_word = nlp(i).vector.reshape(1, -1) 
    Result = list(nn.kneighbors(test_word))
    Result = Result[1]
    Result = Result[0]
    Result = int(Result[0])
    Result = Result -1
    kind_result = df_kinds.query(f"id_ == {Result}")
    kind_result= kind_result["kind"]
    kind_result = dict(kind_result)
    kind_result_es = kind_result[Result]  # kind clave
    kind_result_en = list(csv.loc[Result:Result,"english_words",])[0]
    loc_ = ent_
    List_kind_.append(kind_result_en)

for i in  List_adj_:

    test_word = nlp(i).vector.reshape(1, -1) 
    Result = list(nn.kneighbors(test_word))
    Result = Result[1]
    Result = Result[0]
    Result = int(Result[0])
    Result = Result -1
    kind_result = df_kinds.query(f"id_ == {Result}")
    kind_result= kind_result["kind"]
    kind_result = dict(kind_result)
    kind_result_es = kind_result[Result]  # kind clave
    kind_result_en = list(csv.loc[Result:Result,"english_words",])[0]
    loc_ = ent_    
    List_kind_.append(kind_result_en)

List_kind_ = list(dict.fromkeys(List_kind_)) #elimina duplicados



# #####################################
  # RESULTADOS
# ####################################
#palabras extraídas del texto:

List_noun_
List_adj_
ent_

print(f"Las palabras extraídas del téxto son: lista de nombres:{List_noun_}, lista de nombres y adjetivos:{List_adj_},localización: {ent_}" )

#  Variables de lugar y kinds:

loc_
List_kind_

print(f"Las palabras con las que vamos a realizar la quaery son: lista de kinds:{List_kind_},localización: {loc_}" )




















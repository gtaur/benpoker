import tests_function as f
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import datetime

## CONNECTION SETUP ##
uri = "mongodb+srv://bambarlow92:Paracetamolo24!@clusterpoker.c06sqkx.mongodb.net/?retryWrites=true&w=majority&appName=clusterPoker"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Seleziona il database
db = client['poker_s3']

# Seleziona la collezione
mdbclass = db['classifica']

ycoll = db['history']

df_class = f.coll_to_df(mdbclass)
print (df_class.head())

# Convertiamo il DataFrame in un dizionario di dizionari
dict_of_dicts = df_class.to_dict(orient='index')
# Aggiungiamo il campo data
dict_of_dicts['data di registrazione'] = "29-08-2024"
# Stampa il dizionario risultante
print(dict_of_dicts)
my_dict_with_str_keys = {str(k): v for k, v in dict_of_dicts.items()}
print(my_dict_with_str_keys['data di registrazione'])

# Convertiamo il dizionario di dizionari in un DataFrame
#df_t = pd.DataFrame(dict_of_dicts).T  # .T per trasporre e avere l'indice corretto

# Stampa il DataFrame risultante
#print(df_t)



ycoll.insert_one(my_dict_with_str_keys)

#query = {'data di registrazione': "29-08-2024"}

result = ycoll.find()

# Stampa i risultati
for document in result:
    print(document)

#document = ycoll.find_one(query)

# Stampa il documento trovato
#print(document)

"""


# # Carica il file Excel in un DataFrame
# df = pd.read_excel("files/Benpoker.xlsx",sheet_name="classifiche")
# classifica_aggiornata_20240830_120309
# #carica csv
# # file_path = "files/matches.csv"  # Sostituisci con il percorso corretto del tuo file Excel
# # df = pd.read_csv(file_path,sep=";")

# print(df.head()) # check print


# ### CARICA DF IN MONGO ####

# data_dict = df.to_dict("records")
# collection.insert_many(data_dict)

# print("Dati inseriti correttamente in MongoDB!")

#f.collection_update_by_field(xcollection,'Giocatore','Antonio Rafaschieri','Punti',600)

excel_file = "files/classifica_aggiornata_20240830_120309.xlsx"
xl = pd.ExcelFile(excel_file)

df = xl.parse(sheet_name='classifiche',index_col=False)

#df = pd.read_excel("files/classifica_aggiornata_20240830_120309.xlsx",sheet_name="classifiche")

f.aggiorna_player_da_dataframe_su_mdb(xcollection,df)

###     QUERIES DI RETRIVAL   ####


# Definisci il filtro per trovare il documento
filtro = {"Giocatore": "Antonio Rafaschieri"}

# Trova un documento
documento = xcollection.find_one(filtro)

# Verifica se è stato trovato un documento
if documento:
    print("\n\n Documento trovato:", documento)
else:
    print(" \n\n Nessun documento trovato.")


# Esegui una query
# Ad esempio, trovare tutti i documenti nella collezione
# result = xcollection.find()

# # Stampa i risultati
# for document in result:
#     print(document)


### CONVERTI COLLECTION IN DATAFRAME ###

# Recupera tutti i documenti dalla collezione
#documenti = list(xcollection.find())  # Usa list() per convertire il cursore in una lista di documenti

# Converti la lista di documenti in un DataFrame
#df = pd.DataFrame(documenti)

# Visualizza il DataFrame
#print(df.head())  # Mostra le prime righe del DataFrame

# # Puoi anche fare query più specifiche
# query = {"campo": "valore"}
# specific_result = collection.find(query)

# # Stampa i risultati specifici
# for document in specific_result:
#     print(document)


"""




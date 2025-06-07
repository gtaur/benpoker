import shutil
import os
import datetime 
#from datetime import date
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
from bson import ObjectId


def mongo_conn(collezione):
   ### da parametrizzare anche uri e db


    ## CONNECTION SETUP ##
    uri = "mongodb+srv://bambarlow92:Paracetamolo24!@clusterpoker.c06sqkx.mongodb.net/?retryWrites=true&w=majority&appName=clusterPoker"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Seleziona il database
    db = client['poker_s3']

    # Seleziona la collection
    collection = db[collezione]

    return collection

def coll_to_df(coll):
   ### CONVERTI COLLECTION IN DATAFRAME ###

# Recupera tutti i documenti dalla collezione
    documenti = list(coll.find())  # Usa list() per convertire il cursore in una lista di documenti

    # Converti la lista di documenti in un DataFrame
    df = pd.DataFrame(documenti)

    return df

def add_col_position(df):

        # Aggiungere la colonna 'Posizione' che è l'indice + 1
    df = df.assign(Posizione=lambda x: x.index)
    # Portare la colonna 'Posizione' davanti a tutte le altre
    colonne = ['Posizione'] + [col for col in df.columns if col != 'Posizione']
    df = df[colonne]

    return df

def rimuovi_elemento(lista):
  print("Lista di tutti i giocatori: \n")
  for elemento in lista:
    print(elemento)
  print("\n")
  risposta = input("Vuoi rimuovere un giocatore? (sì/no): ").lower()
  if risposta == "sì":
    elemento_da_rimuovere = input("Quale elemento vuoi rimuovere? ")
    if elemento_da_rimuovere in lista:
      lista.remove(elemento_da_rimuovere)
      print("Elemento rimosso con successo!")
    else:
      print("L'elemento specificato non è presente nella lista.")
  elif risposta == "no":
    print("Nessun elemento rimosso.")
  else:
    print("Risposta non valida. Riprova.")

def create_tables(list):
    lista_pari = []
    lista_dispari = []
   
    for indice, valore in enumerate(list):
        if indice % 2 == 0:
            lista_pari.append(valore)
        else:
            lista_dispari.append(valore)

    return lista_pari,lista_dispari

def sposta_key_dict_in_cima(chiave_da_spostare,dizionario):
   if chiave_da_spostare in dizionario:
    # Estrai il valore della chiave da spostare
    valore_da_spostare = dizionario.pop(chiave_da_spostare)
    
    # Ricostruisci il dizionario con la chiave spostata in cima
    dizionario = {chiave_da_spostare: valore_da_spostare, **dizionario}
    

    return dizionario


def load_ml_mdb(df):
    
    df = df.drop(['_id'],axis=1)
    # Filtriamo il DataFrame per mantenere solo le righe in cui master legue  è 1
    master_league_df = df[df['MasterLeague'] != 0]
    master_league_df = master_league_df.sort_values(by='Punti',ascending=False)
    mlx = master_league_df.drop(['MasterLeague'],axis=1)
    ml = mlx.reset_index(drop=True)
    ml.index = ml.index + 1

    return ml


def load_chart_mdb(df):

    df = df.drop(['_id'],axis=1)
    classifica_df = df.sort_values(by='Punti', ascending=False)
    cfx = classifica_df.drop(['MasterLeague'],axis=1)
    cf = cfx.reset_index(drop=True)
    cf.index = cf.index + 1

    return cf



def update_mday_by_dict(dict,nome_giocatore, posizione):

    message = True


    posiz = str(posizione)
    valoriDict = dict.values()
    valoriDict_= [elemento for elemento in valoriDict if elemento is not None]

  
    
    # Verifica se dict[posiz] è già presente in valoriDict_
    if nome_giocatore not in valoriDict_ and dict[posiz] == None:
        dict[posiz] = nome_giocatore
    else:
        message=False
      

    return dict,message

def create_match_dict(matchday):
    dizio = {
    "matchday": matchday,
    "data": None,
    "1": None,
    "2": None,
    "3": None,
    "4": None,
    "5": None,
    "6": None,
    "7": None,
    "8": None,
    "9": None,
    "10": None,
    "11": None,
    "12": None,
    "13": None,
    "14": None,
    "15": None
        }


    return dizio

def collection_update_by_field(collection,campo,valcamp,fieldToUpdate,new_val):

    # Definisci il filtro per selezionare il documento
    filtro = {campo: valcamp}

    # Definisci l'operazione di aggiornamento
    aggiornamento = {"$set": {fieldToUpdate: new_val}}

    # Aggiorna il documento
    collection.update_one(filtro, aggiornamento)

    print("Documento aggiornato con successo!")

def aggiorna_player_da_dataframe_su_mdb(collection, dataframe):

# Itera sulle righe del DataFrame
    for _, row in dataframe.iterrows():
        # Salva la riga in un dizionario
        dizionario_riga = row.to_dict()

        # Costruisci il filtro e l'aggiornamento per ogni riga
        filtro = {"Giocatore": dizionario_riga["Giocatore"]}
        
        # Prepara i dati da aggiornare (escludendo il campo "Giocatore" dal dizionario degli aggiornamenti)
        aggiornamenti = {k: v for k, v in dizionario_riga.items() if k != "Giocatore"}
        
        # Definisci l'operazione di aggiornamento
        operazione_aggiornamento = {"$set": aggiornamenti}
        
        # Aggiorna il documento
        result = collection.update_one(filtro, operazione_aggiornamento)
        
        # Verifica se l'aggiornamento è andato a buon fine
        if result.matched_count > 0:
            print(f"Documento con Giocatore {dizionario_riga['Giocatore']} aggiornato con successo!")
        else:
            print(f"Nessun documento trovato con Giocatore {dizionario_riga['Giocatore']}.")

def saveSnapshot(coll,dataframe):
    #mex = False

    dict_of_dicts = dataframe.to_dict(orient='index')
    today = datetime.datetime.now().strftime('%d-%m-%Y')
    dict_of_dicts['data di registrazione'] = today
    my_dict_with_str_keys = {str(k): v for k, v in dict_of_dicts.items()}
    
    coll.insert_one(my_dict_with_str_keys)

def storicoPlayer(collection, nome_giocatore):
    # Lista per memorizzare i risultati
    risultati_lista = []

    # Esegui la query per trovare tutti i documenti nella collezione
    for doc in collection.find():
        posizione_giocatore = None

        # Cerca tra le chiavi del documento
        for chiave, valore in doc.items():
            # Se il valore è il nome del giocatore, salva la posizione
            if valore == nome_giocatore:
                posizione_giocatore = chiave
                break  # Una volta trovato, non serve continuare a cercare

        # Se il giocatore è presente, salva il risultato
        if posizione_giocatore:
            risultati_lista.append({
                'Giornata': doc.get('matchday'),
                'Data': doc.get('data'),
                'Posizione': posizione_giocatore + '°'
            })

    # Converti la lista dei risultati in un DataFrame di Pandas
    df = pd.DataFrame(risultati_lista)

    return df

def creaDFPartiteglobal (coll):
   # DataFrame vuoto per accumulare tutti i dati
    df_completo = pd.DataFrame()

# Ottieni tutti i documenti della collection
    documenti = coll.find()

# Itera su ogni documento
    for doc in documenti:
        # Converti il documento in un DataFrame
        df = pd.DataFrame([doc])
        
        # Rimuovi la colonna '_id'
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])
        
        # Trasponi il DataFrame
        df_transposta = df.T
        
        # Aggiungi il DataFrame trasposto al DataFrame completo
        df_completo = pd.concat([df_completo, df_transposta], axis=1)

        df_completo = df_completo.fillna()

# Mostra il DataFrame completo
    print(df_completo)

    return df_completo
   
def reset_fields_to_zero(collection, fields_to_reset):
    """
    Imposta a zero alcuni campi di ogni documento nella collezione MongoDB.

    :param collection: La collezione MongoDB in cui aggiornare i documenti.
    :param fields_to_reset: Lista dei nomi dei campi che devono essere impostati a zero.
    """
    # Crea un dizionario con i campi da aggiornare impostati a zero
    update_fields = {field: 0 for field in fields_to_reset}

    # Aggiorna tutti i documenti nella collezione impostando i campi specificati a zero
    result = collection.update_many({}, {'$set': update_fields})

    # Stampa il numero di documenti aggiornati
    print(f"{result.modified_count} documenti aggiornati.")

def get_all_keys(collection):
    """
    Legge tutte le chiavi uniche presenti nei documenti di una collezione MongoDB.

    :param collection: La collezione MongoDB da cui leggere i documenti.
    :return: Una lista contenente tutte le chiavi uniche.
    """
    all_keys = []  # Lista per raccogliere tutte le chiavi uniche

    # Itera su tutti i documenti della collezione
    for document in collection.find():
        # Aggiunge le chiavi del documento corrente alla lista, se non già presenti
        for key in document.keys():
            if key not in all_keys:
                all_keys.append(key)
    
    return all_keys

def reset_all_players(coll): ### va corretta

    lista = get_all_keys(coll)
    lista.remove('Giocatore')
    lista.remove('_id')

    for elem in lista:
        reset_fields_to_zero(coll,elem)

def print_all_documents(collection):

    """
    Stampa tutti i documenti presenti in una collezione MongoDB.

    :param collection: La collezione MongoDB da cui leggere i documenti.
    """
    # Itera su tutti i documenti della collezione
    for document in collection.find():
        # Stampa il documento
        print(document)

def delete_all_documents(collection):

    # Cancellazione di tutti i documenti
    result = collection.delete_many({})

    # Stampa del numero di documenti cancellati
    print(f"{result.deleted_count} documenti cancellati dalla collezione '{collection}'.")

def copia_giocatori_e_crea_documenti(source_collection,target_collection):


    """
    Legge tutti i nomi dal campo 'giocatore' di ogni documento nella collezione sorgente
    e crea nuovi documenti nella collezione di destinazione con chiavi predefinite e valori iniziali a zero.

    :param source_db: Nome del database sorgente.
    :param source_collection_name: Nome della collezione sorgente da cui leggere i giocatori.
    :param target_db: Nome del database di destinazione.
    :param target_collection_name: Nome della collezione di destinazione in cui inserire i nuovi documenti.
    """

    
    # Lettura dei nomi completi dei giocatori dalla collezione sorgente
    lista_giocatori = [
        f"{doc['Nome']} {doc['Cognome']}"
        for doc in source_collection.find()
        if 'Nome' in doc and 'Cognome' in doc
    ]

    # Creazione dei nuovi documenti nella collezione di destinazione
    nuovi_documenti = []
    for giocatore in lista_giocatori:
        nuovo_documento = {
            'Giocatore': giocatore,
            'Punti': 0,
            'Sconfitte': 0,
            'PG': 0,
            'Tot Cash Vinto': 0,
            'Podi': 0,
            'MasterLeague': 0
        }
        nuovi_documenti.append(nuovo_documento)
        print(nuovo_documento)

    # Inserimento dei nuovi documenti nella collezione di destinazione
    if nuovi_documenti:
        target_collection.insert_many(nuovi_documenti)
        print(f"{len(nuovi_documenti)} documenti inseriti nella collezione '{target_collection}'.")
    else:
        print("Nessun documento da inserire.")


def delete_all_docs_minus_one_by_id(coll,id_doc):


    # ID del documento da mantenere (deve essere di tipo ObjectId)

    id_to_keep = ObjectId(id_doc)  # Sostituiscilo con il tuo ObjectId

    # Cancella tutti i documenti tranne quello con l'ID specifico
    coll.delete_many({"_id": {"$ne": id_to_keep}})

    print("Tutti i documenti sono stati cancellati tranne quello con _id:", id_to_keep)

def clean_players_chart(collection):

    list_keys = ['Punti', 'Sconfitte', 'PG', 'Tot Cash Vinto', 'Podi', 'MasterLeague']

    for key in list_keys:
        collection.update_many({}, {"$set": {key: 0}})

print("Campo aggiornato in tutti i documenti!")

def clean_single_doc(collection,keys_list):
        
    for key in keys_list:
        collection.update_many({}, {"$set": {key: None}})


def key_values_tolist(collection):
    # Trova un documento qualsiasi
    doc = collection.find_one()

    if doc:
        # Ottieni i nomi dei campi (chiavi) e li salva in una lista
        lista_campi = list(doc.keys())
        print("Campi trovati:", lista_campi)
    else:
        print("Nessun documento trovato nella collection.")

    return lista_campi


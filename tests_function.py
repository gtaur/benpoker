import shutil
import os
from datetime import datetime
from datetime import date
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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


def load_data_xl(excel_file):
    # Carica i dati dal file Excel
    xl = pd.ExcelFile(excel_file)
    
    # Supponiamo che il primo foglio contenga i dati di classifica e master league
    classifica_df = xl.parse(sheet_name='classifiche',index_col=False)
    classifica_df = classifica_df.sort_values(by='Punti', ascending=False)
    cfx = classifica_df.drop(['MasterLeague'],axis=1)
    cf = cfx.reset_index(drop=True)
    cf.index = cf.index + 1
    return cf

def sposta_file(percorso_file, destinazione):
    """
    Sposta un file da una directory a un'altra.

    :param percorso_file: Percorso completo del file da spostare.
    :param destinazione: Directory di destinazione dove spostare il file.
    """
    try:
        # Verifica che il file esista
        if not os.path.isfile(percorso_file):
            raise FileNotFoundError(f"Il file '{percorso_file}' non esiste.")
        
        # Crea la directory di destinazione se non esiste
        os.makedirs(destinazione, exist_ok=True)
        
        # Costruisci il percorso di destinazione del file
        nome_file = os.path.basename(percorso_file)
        percorso_destinazione = os.path.join(destinazione, nome_file)
        
        # Sposta il file
        shutil.move(percorso_file, percorso_destinazione)
        
        #print(f"File '{percorso_file}' spostato in '{percorso_destinazione}'")
    
    except Exception as e:
        print(f"Errore: {e}")

def sposta_e_rinomina_file(percorso_file_sorgente, percorso_directory_destinazione):
    """
    Sposta un file in una directory di destinazione e rinomina il file aggiungendo un timestamp.

    :param percorso_file_sorgente: Percorso del file sorgente da spostare e rinominare.
    :param percorso_directory_destinazione: Directory di destinazione per il file.
    :return: Il percorso completo del file spostato e rinominato.
    """
    # Ottieni il nome del file e l'estensione
    nome_file = os.path.basename(percorso_file_sorgente)
    nome_file_senza_estensione, estensione = os.path.splitext(nome_file)

    # Ottieni il timestamp corrente
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Costruisci il nuovo nome del file
    nome_file_nuovo = f"{nome_file_senza_estensione}_{timestamp}{estensione}"

    # Costruisci il percorso completo del file di destinazione
    percorso_file_destinazione = os.path.join(percorso_directory_destinazione, nome_file_nuovo)

    # Assicurati che la directory di destinazione esista, altrimenti creala
    if not os.path.exists(percorso_directory_destinazione):
        os.makedirs(percorso_directory_destinazione)

    # Sposta e rinomina il file
    shutil.move(percorso_file_sorgente, percorso_file_destinazione)

    return percorso_file_destinazione

def rinomina_file_con_timestamp(percorso_file):
    """
    Rinomina un file aggiungendo un timestamp al nome del file.

    :param percorso_file: Percorso completo del file da rinominare.
    """
    try:
        # Verifica che il file esista
        if not os.path.isfile(percorso_file):
            raise FileNotFoundError(f"Il file '{percorso_file}' non esiste.")
        
        # Ottieni il timestamp corrente
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Estrai il nome e l'estensione del file
        directory, nome_file = os.path.split(percorso_file)
        nome_base, estensione = os.path.splitext(nome_file)
        
        # Crea il nuovo nome del file con il timestamp
        nuovo_nome = f"{nome_base}_{timestamp}{estensione}"
        nuovo_percorso = os.path.join(directory, nuovo_nome)
        
        # Rinomina il file
        os.rename(percorso_file, nuovo_percorso)
        print(f"File '{percorso_file}' rinominato in '{nuovo_percorso}'")
    
    except Exception as e:
        print(f"Errore: {e}")

def get_most_recent_file(directory, prefix):
    # Elenco di tutti i file nella directory specificata
    files = os.listdir(directory)
    
    # Filtra i file che iniziano con il prefisso specificato
    filtered_files = [file for file in files if file.startswith(prefix)]
    
    if not filtered_files:
        return None
    
    # Trova il file più recente
    most_recent_file = None
    most_recent_time = None
    
    for file in filtered_files:
        file_path = os.path.join(directory, file)
        file_mtime = os.path.getmtime(file_path)  # Ottiene il timestamp di modifica del file
        
        if most_recent_time is None or file_mtime > most_recent_time:
            most_recent_file = file
            most_recent_time = file_mtime
    
    return most_recent_file

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

def load_data_master_l(excel_file):
    # Carica i dati dal file Excel
    xl = pd.ExcelFile(excel_file)
    
    # Supponiamo che il primo foglio contenga i dati di classifica e master league
    classifica_df = xl.parse(sheet_name='classifiche',index_col=False)
    # Filtriamo il DataFrame per mantenere solo le righe in cui master legue  è 1
    master_league_df = classifica_df[classifica_df['MasterLeague'] != 0]
    master_league_df = master_league_df.sort_values(by='Punti',ascending=False)
    mlx = master_league_df.drop(['MasterLeague'],axis=1)
    ml = mlx.reset_index(drop=True)
    ml.index = ml.index + 1

    
    return ml

def load_data_home(excel_file):
    # Carica i dati dal file Excel
    xl = pd.ExcelFile(excel_file)
    
    # Supponiamo che il primo foglio contenga i dati di classifica e master league
    classifica_df = xl.parse(sheet_name='classifiche',index_col=False)
    classifica_df = classifica_df.sort_values(by='Punti', ascending=False)
    cfx = classifica_df.drop(['MasterLeague'],axis=1)
    cf = cfx.reset_index(drop=True)
    cf.index = cf.index + 1
    return cf

# f con mongo

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

def clean_matches_mdb(df):
   df = df.drop(['_id'],axis=1)
   df = df.fillna('')
   return df


def update_mday_by_dict(df,dict,nome_giocatore, posizione,data):

    message = True
    penultimo_index = df.index[-1]
    #trova e inserisci giorno match:
    dict["matchday"] = int(df.at[penultimo_index,"matchday"]) + 1
    dict["data"] = data #.strftime("%d/%m/%Y")
    posiz = str(posizione)
    valoriDict = dict.values()
    valoriDict_= [elemento for elemento in valoriDict if elemento is not None]

  
    
    # Verifica se dict[posiz] è già presente in valoriDict_
    if nome_giocatore not in valoriDict_ and dict[posiz] == None:
        dict[posiz] = nome_giocatore
    else:
        message=False
      

    return dict,message


def create_match_dict():
    dizio = {
    "matchday": None,
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

        


     

#######################################
############### TEST FX ################
########################################

""" 
classifica_df = load_data_xl("files/classifica_aggiornata_20240728_182339.xlsx")

cldf = classifica_df

cldf.sort_values(by='Punti', ascending=False)
# Visualizza il DataFrame
print("DataFrame:")
print(cldf)

# Creazione del dizionario con l'indice come chiave e Giocatore come valore
dizionario = cldf['Giocatore'].to_dict()

print("\nDizionario:")
print(dizionario)

today = date.today()

dizionario['data'] = today

print(dizionario)


dictupdated = sposta_key_dict_in_cima("data",dizionario)

print(dictupdated)


# Carica il file CSV esistente
matches_file_path = 'files/matches_test.csv'
mm_df = pd.read_csv(matches_file_path, sep=';')

# Creare una riga vuota
empty_row = pd.DataFrame([[''] * len(mm_df.columns)], columns=mm_df.columns)

mm_df = pd.concat([mm_df, empty_row], ignore_index=True)

print(mm_df)

last_index = mm_df.index[-1]

mm_df.at[last_index, 'data'] = dictupdated["data"].strftime("%d/%m/%Y")
for i in range(1, 16):
   mm_df.at[last_index, str(i)] = dictupdated[i]

print(mm_df)

mm_df.to_csv('files/matches_test.csv', sep=';', index=False)

"""
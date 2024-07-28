import shutil
import os
from datetime import datetime

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

# Esempio di utilizzo della funzione

# percorso_file_sorgente = 'tests/asd.txt'
# percorso_directory_destinazione = 'tests/prova/'

# percorso_file_nuovo = sposta_e_rinomina_file(percorso_file_sorgente, percorso_directory_destinazione)
# print(f"File spostato e rinominato in: {percorso_file_nuovo}")

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
#import pandas as pd

import os
from PIL import Image

def ridimensiona_png(directory):
    # Trova tutti i file PNG nella directory
    png_files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
    
    # Se non ci sono file PNG nella directory, termina lo script
    if not png_files:
        print("Nessun file PNG trovato nella directory.")
        return

    # Inizializza le variabili per il PNG più piccolo
    min_width, min_height = float('inf'), float('inf')
    min_image = None

    # Trova il PNG più piccolo
    for png_file in png_files:
        img_path = os.path.join(directory, png_file)
        with Image.open(img_path) as img:
            width, height = img.size
            if width * height < min_width * min_height:
                min_width, min_height = width, height
                min_image = img

    print(f"Il PNG più piccolo è {min_width}x{min_height}.")

    # Ridimensiona tutti i PNG alle dimensioni del PNG più piccolo
    for png_file in png_files:
        img_path = os.path.join(directory, png_file)
        with Image.open(img_path) as img:
            resized_img = img.resize((min_width, min_height))
            resized_img.save(img_path)
            print(f"{png_file} ridimensionato a {min_width}x{min_height}.")

# Specifica la directory contenente i file PNG
directory = "foto/testsfunction"
ridimensiona_png(directory)







######################################
############# EXECUTION ##############
######################################






"""
# df = load_csv("files/players.csv")
# print(df)

# Carica i dati
classifica_df, master_league_df = load_data('files/Benpoker.xlsx')

print(classifica_df, "\n\n")
print(master_league_df, "\n\n")


# Ciclo principale per l'aggiornamento della classifica
while True:
    # Mostra il DataFrame iniziale
    print("\nClassifica attuale:")
    print(classifica_df)

    print("\nGiocatori disponibili:")
    for i, giocatore in enumerate(classifica_df['Giocatore'], start=1):
        print(f"{i}. {giocatore}")

    # Richiede all'utente di selezionare un giocatore dall'elenco
    scelta = int(input("\nSeleziona il numero del giocatore: "))
    nome_giocatore = classifica_df['Giocatore'].iloc[scelta - 1]

    posizione = int(input("Inserisci la posizione ottenuta nell'ultima giornata (1-8): \n "))
    soldi = int(input("Inserisci il suo guadagno: \n"))

    # Aggiorna il DataFrame
    df_aggiornato = aggiorna_classifica(classifica_df, nome_giocatore, posizione,soldi)

    # Chiede all'utente se vuole continuare o salvare
    continua = input("\nVuoi continuare ad aggiornare la classifica? (s/n): ")
    if continua.lower() != 's':

        break


# Mostra il DataFrame aggiornato
print("\nClassifica aggiornata:")
print(df_aggiornato)

# Scrive il DataFrame aggiornato in un file Excel
file_path = 'outputs/classifica_aggiornata.xlsx'
df_aggiornato.to_excel(file_path, index=False)
print(f"\nLa classifica aggiornata è stata salvata in '{file_path}'")

"""
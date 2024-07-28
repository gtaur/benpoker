import pandas as pd

######################################
############## FUNCTIONS #############
######################################

def load_data(excel_file):
    # Carica i dati dal file Excel
    xl = pd.ExcelFile(excel_file)
    
    # Supponiamo che il primo foglio contenga i dati di classifica e master league
    classifica_df = xl.parse(sheet_name='classifiche',index_col=False)
    classifica_df = classifica_df.sort_values(by='Punti', ascending=False)
    cfx = classifica_df.drop(['MasterLeague'],axis=1)
    cf = cfx.reset_index(drop=True)
    cf.index = cf.index + 1
    # Filtriamo il DataFrame per mantenere solo le righe in cui master legue  è 1
    master_league_df = classifica_df[classifica_df['MasterLeague'] != 0]
    master_league_df = master_league_df.sort_values(by='Punti',ascending=False)
    mlx = master_league_df.drop(['MasterLeague'],axis=1)
    ml = mlx.reset_index(drop=True)
    ml.index = ml.index + 1


    return cf, ml


def load_csv(file):

    df = pd.read_csv(file,index_col=False,sep=";")

    return df

# Funzione per calcolare i punti in base alla posizione
def calcola_punti(posizione):
    punti_posizione = {1: 10, 2: 8, 3: 6, 4: 3, 5: 2, 6: 1}
    return punti_posizione.get(posizione, 0)

# Funzione per aggiornare il DataFrame
def aggiorna_classifica(df, nome_giocatore, posizione,cash):
    punti = calcola_punti(posizione)
    
    if nome_giocatore in df['Giocatore'].values:
        index = df.index[df['Giocatore'] == nome_giocatore].tolist()[0]
        df.at[index, 'PG'] += 1
        df.at[index, 'Punti'] += punti
        df.at[index, 'Tot Cash vinto'] += cash
        
        if posizione == 1 or posizione == 2 or posizione == 3:
            df.at[index, 'Vittorie'] += 1
        else:
            df.at[index, 'Sconfitte'] += 1
    
    return df

######################################
############# EXECUTION ##############
######################################

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
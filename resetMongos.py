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

history = db['history']

matches = db['matches']
players = db['players']



# f.reset_all_players(mdbclass)   #fa un casino da capire perchè
# f.print_all_documents(mdbclass)
# f.delete_all_documents(mdbclass)

#f.copia_giocatori_e_crea_documenti(players,mdbclass)


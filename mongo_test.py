
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
db = client['sample_mflix']

# Seleziona la collezione
collection = db['users']

# Esegui una query
# Ad esempio, trovare tutti i documenti nella collezione
result = collection.find()

# Stampa i risultati
for document in result:
    print(document)

# # Puoi anche fare query più specifiche
# query = {"campo": "valore"}
# specific_result = collection.find(query)

# # Stampa i risultati specifici
# for document in specific_result:
#     print(document)
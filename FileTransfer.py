from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


client = None

def login_mongodb():
    global client
    uri = "mongodb+srv://QuantumCircuitsAdmin:Leonardo1962Aa0800832@cluster0.lhnzioz.mongodb.net/?retryWrites=true&w=majority"
	# Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

	# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        return None
        
        
def get_file(username, file_name):
    global client
    if(client == None):
        client = login_mongodb()
    db = client["DietQuantumCircuits"]
    circuit_files = db["circuit_files"]
    circuit_file = circuit_files.find_one({"username" : username, "file_name":file_name})
    
    return circuit_file
    

def add_file(username, file_name, file_data):
    global client
    
    if(client == None):
        client = login_mongodb()

    db = client["DietQuantumCircuits"]
    circuit_files = db["circuit_files"]
    
    if circuit_files.find_one(file_name):
        print("User already exists.")
        return False
    
    file_data.update(
    {
        'file_name' : file_name,
        'username' : username
    })
    
    filter = { 'file_name': file_name }

    newvalues = { "$set": file_data }
    
    circuit_files.update_one(filter, newvalues)

    return True
    
    
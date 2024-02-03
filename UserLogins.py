from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = None

def login_mongodb():
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

def add_user(username, hash_password):
    global client
    if(client == None):
        client = login_mongodb()
    db = client["DietQuantumCircuits"]
    user_collection = db["credentials"]
    
    if user_collection.find_one({"rcsid": username}):
        print("User already exists.")
        return False
    
    user_data = {
        "username": username,
        "hash_password": hash_password
    }
    user_collection.insert_one(user_data)
    print("User added successfully.")
    return True

def find_user(username, hashed_password):
    global client
    if(client == None):
        client = login_mongodb()
    db = client["DietQuantumCircuits"]
    user_collection = db["credentials"]
    user_data = user_collection.find_one({"rcsid": username})
    
    if user_data:
        if(user_data["sha256pwd"] == hashed_password):
            return user_data
        return None
    else:
        return None

import hashlib
password = "Leonardo*1962Aa0800832"
hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
print(find_user("sheild", hashed_password))
print(find_user("sheild", hashed_password))
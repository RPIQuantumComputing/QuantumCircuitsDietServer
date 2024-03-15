from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import jwt
import secrets

import datetime

client = None

JWT_SECRET = "test"

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
    user_data = user_collection.find_one({"username": username})
    
    if user_data:
        if(user_data["hash_password"] == hashed_password):
            return user_data
        return None
    else:
        return None

def user_login(username, hashed_password):
    global client
    if(client == None):
        client = login_mongodb()
    db = client["DietQuantumCircuits"]

    if(find_user(username,hashed_password) == None):
        return None

    user_sessions = db["user_sessions"]

    jwt_sesion = {
        'username' : username,
        'expiration' : int( (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d%H%M%S") ),
        'nonce' : secrets.token_hex()
    }

    encoded_jwt = jwt.encode(jwt_sesion, JWT_SECRET, algorithm="HS256")

    session_data = {
        "username": username,
        "session_cookie" :encoded_jwt
    }

    user_sessions.update_one({"username":username},{"$set":session_data},upsert=True)

    return encoded_jwt
    

def verify_session(session_cookie):
    global client
    if(client == None):
        client = login_mongodb()
    db = client["DietQuantumCircuits"]
    user_sessions = db["user_sessions"]
    user_session = user_sessions.find_one({"session_cookie":session_cookie})

    if(user_session):
        session = jwt.decode(user_session['session_cookie'], JWT_SECRET, algorithms=["HS256"])

        if(session['expiration'] <= int( datetime.datetime.now().strftime("%Y%m%d%H%M%S") )):
            return False
        return True
    else:
        return False


if __name__ == '__main__':
    import hashlib
    # password = "Leonardo*1962Aa0800832"
    # hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # print(find_user("sheild", hashed_password))
    # print(find_user("sheild", hashed_password))

    test_password = "test123"
    hashed_test = hashlib.sha256(test_password.encode('utf-8')).hexdigest()
    print(find_user("test",hashed_test))
    #print(user_login("test",hashed_test))
    print(verify_session("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHBpcmF0aW9uIjoyMDI0MDMxNjE2NDExNywibm9uY2UiOiJlZTA0MTNlODNjNTUwNzlhYWU1NzYwNTRmMGVmY2IzMTBmOTMyMDRmZGNhYzZhNDU4MDlhYTZlNDc1OThhNzZhIn0.qak092nzGrBFXlNOAWEhDeu_tQ0KDKajNxEDmdE0sCM"))
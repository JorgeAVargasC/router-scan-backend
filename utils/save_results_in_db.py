from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def save_results_in_db(data):
    uri = "mongodb+srv://root:1234@cluster0.xvqlwek.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        db = client['router_scan_db']
        collection = db['router_scan_results']
        
        collection.insert_one(data)
        
    except Exception as e:
        print(e)
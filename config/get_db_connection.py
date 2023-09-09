from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_db_connection():
    uri = "mongodb+srv://root:1234@cluster0.xvqlwek.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db = client['router_scan_db']
        return db

    except Exception as e:
        print(e)
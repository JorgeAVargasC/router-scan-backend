from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
 
load_dotenv()

from dotenv import dotenv_values
 
env = dotenv_values(".env") 

USERNAME = env["USERNAME"]
PASSWORD = env["PASSWORD"]
HOSTNAME = env["HOSTNAME"]

def db_connection():
    uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOSTNAME}/?retryWrites=true&w=majority"
    print(uri)
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        db = client['router_scan_db']
        collection = db['router_scan_results']
        
        return collection

    except Exception as e:
        print(e)
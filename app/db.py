from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()
master = db["organizations"]

class DB:
    @staticmethod
    def master(): return master
    
    @staticmethod
    def create_collection(name: str):
        if name not in db.list_collection_names():
            db.create_collection(name)
    
    @staticmethod
    def collection(name: str):
        return db[name]
    
    @staticmethod
    def drop(name: str):
        if name in db.list_collection_names():
            db[name].drop()
    
    @staticmethod
    def rename(old: str, new: str):
        if old in db.list_collection_names():
            db[old].rename(new, dropTarget=True)
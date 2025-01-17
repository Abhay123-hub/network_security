import os
import sys
import json
from dotenv import load_dotenv


load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
           raise NetworkSecurityException(e,sys)
    def csv_to_json_converter(self,data_path):
        try:
            data = pd.read_csv(data_path)
            data.reset_index(drop = True,inplace = True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_mongodb(self,database,collection,records):
      try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.colection = self.database[self.collection]
            self.collection.insert_many(self.records)
            
            
      except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    data_path = "Network_Data\phisingData.csv"
    database = "sample_mflix"
    collection = "my_collection"
    network = NetworkDataExtract()
    records = network.csv_to_json_converter(data_path)
    network.insert_data_mongodb(database,collection,records)
    

    




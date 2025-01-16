from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pymongo
from typing import List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_data_frame(self):
        "jsut to read the data from mongo db"
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace = True)
           
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_data_into_feature(self,dataframe:pd.DataFrame):
        try:
            feature_store_path = self.data_ingestion_config.feature_store_path
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_path,header=True,index = False)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set = train_test_split(
                dataframe,test_size = self.data_ingestion_config.train_test_ration
            )
            logging.info("performed train and test split on the dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok = True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index = False,header = True)

            dir_path_test = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path_test,exist_ok = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index = False,header = True)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
        

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_data_frame()
            self.export_data_into_feature(dataframe)
            self.split_data_as_train_test(dataframe)
            artifact = DataIngestionArtifact(test_data_path=self.data_ingestion_config.testing_file_path,
                                             train_data_path=self.data_ingestion_config.training_file_path)
            return artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
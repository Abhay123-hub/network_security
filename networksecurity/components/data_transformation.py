import numpy as np 
import pandas as pd
import os,sys
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.constants.trainining_pipeline import TARGET_COLUMN
from networksecurity.constants.trainining_pipeline import DATA_TRANSFORMATION_INPUT_PARAMS
from networksecurity.entity.artifact_entity import (DataValidationArtifact,DataTransformationArtifact)

from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils3 import save_numpy_array
from networksecurity.utils.main_utils.utils4 import save_object



##now creating data trasnformation class
class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact= data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def get_data_transformer_object(cls) ->Pipeline:
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_INPUT_PARAMS)
            processor = Pipeline([("imputer",imputer)])
            return processor
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initate data transformation")
        try:
            logging.info("starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.validation_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.validation_test_file_path)
            ## training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            logging.info("getting to data transformation object")
            processor = self.get_data_transformer_object()
            processor_object = processor.fit(input_feature_train_df)
            transformed_input_feature_train_df = processor_object.transform(input_feature_train_df)
            save_object("final_model/processor.pkl",processor_object)
            
            
            transformed_input_feature_test_df = processor_object.transform(input_feature_test_df) ## this is in numpy array format
  
            train_arr = np.c_[transformed_input_feature_train_df,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_feature_test_df,np.array(target_feature_test_df)]

            ## saving both the train array and test array
            save_numpy_array(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path,processor_object)

            ## now preparing artifacts for my data transformation PipeLine
            transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            return transformation_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)

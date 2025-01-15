from networksecurity.entity.config_entity import ValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.trainining_pipeline import SCHEMA_FILE_PATH
import sys,os
from scipy.stats import ks_2samp
import pandas as pd
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.utils.main_utils.utils2 import write_yaml_file

## i need to read the schema file 

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 validation_config:ValidationConfig):
        try:
            self.validation_config = validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame) ->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            if number_of_columns == len(dataframe.columns):
                return True
            return False
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05) ->bool:
        try:
            status = True ## by  default
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if is_same_dist.pvalue>= threshold:
                     is_found = False ## no change in drift found
                else:
                    is_found = True
                    status = False ## change in drift was found between both the datasets
                ## updating the report on base of the current column
                report.update({column:{"drift_status":is_found,
                                         "p_value":float(is_same_dist.pvalue)}})
            drift_report_file_path = self.validation_config.drift_report_file_path
            ## create the directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content = report)
            
                    
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_data_path
            test_file_path = self.data_ingestion_artifact.test_data_path
            ## read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            ## now validate the number of columns
            status1 = self.validate_number_of_columns(train_dataframe)
            if not status1:
                error_message = f"Train dataframe does not contain all the columns"
            status2 = self.validate_number_of_columns(test_dataframe)
            if not status2:
                error_message = f"Test dataframe does not contain all the columns"
            ## let us check the data drift
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            path_dir = os.path.join(self.validation_config.valid_train_file_path)
            dir_path = os.path.dirname(path_dir)
            os.makedirs(dir_path,exist_ok = True)
            train_dataframe.to_csv(self.validation_config.valid_train_file_path,header=True,index=False)
            path_dir = os.path.join(self.validation_config.valid_train_file_path)
            dir_path = os.path.dirname(path_dir)
            os.makedirs(dir_path,exist_ok = True)
            test_dataframe.to_csv(self.validation_config.valid_test_file_path)

            ## finally creating the data validation artifact
            ## which will be containing some information of the result which i got from the above code
            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                validation_train_file_path = self.validation_config.valid_train_file_path,
                validation_test_file_path = self.validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invlaid_test_file_path=None,
                drift_report_file_path=self.validation_config.drift_report_file_path
            )
            return data_validation_artifact





        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
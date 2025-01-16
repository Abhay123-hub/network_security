from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipeLineConfig,ValidationConfig,DataTransformationConfig

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
import sys

## now finally executing my data ingestion pipeline
if __name__ == "__main__":
    try:
        logging.info("data ingestion started")
        training_config = TrainingPipeLineConfig()
        data_ingestion_config = DataIngestionConfig(training_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("data ingestion completed")
        logging.info("data validation started")
        data_validation_config = ValidationConfig(training_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                        validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("data validation completed")
        logging.info("Data transformation started")
        data_transformation_config=DataTransformationConfig(training_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                 data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    

    

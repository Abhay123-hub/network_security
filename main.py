from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipeLineConfig,ValidationConfig

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
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
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    

    

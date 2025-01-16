from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipeLineConfig,ValidationConfig,DataTransformationConfig,ModelTrainerConfig

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
import sys

## now finally executing my data ingestion pipeline
if __name__ == "__main__":
    try:
        logging.info("Data Ingestion started")
        training_config = TrainingPipeLineConfig()
        data_ingestion_config = DataIngestionConfig(training_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data Ingestion completed")
        logging.info("Data Validation started")
        data_validation_config = ValidationConfig(training_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                        validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Validation completed")
        logging.info("Data Transformation started")
        data_transformation_config=DataTransformationConfig(training_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                 data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation completed")
        
        logging.info("Model Trainer Pipeline started")
        model_trainer_config = ModelTrainerConfig(training_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
        logging.info("Model Trainer PipeLine Completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    

    

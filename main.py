from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipeLineConfig

from networksecurity.components.data_ingestion import DataIngestion
import sys

## now finally executing my data ingestion pipeline
if __name__ == "__main__":
    training_config = TrainingPipeLineConfig()
    data_ingestion_config = DataIngestionConfig(training_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)

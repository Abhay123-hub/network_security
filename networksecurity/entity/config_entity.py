from datetime import datetime
import os
from networksecurity.constants import trainining_pipeline

print(trainining_pipeline.PIPELINE_NAME)
print(trainining_pipeline.ARTIFACT_DIR)

class TrainingPipeLineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipline_name = trainining_pipeline.PIPELINE_NAME
        self.artifact_name = trainining_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp:str  = timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipeLineConfig):
        self.data_ingestion_dir:str = os.path.join(
         training_pipeline_config.artifact_dir,trainining_pipeline.DATA_INGESTION_DIR_NAME   
        )
        self.feature_store_path:str = os.path.join(
            self.data_ingestion_dir,trainining_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,trainining_pipeline.FILE_NAME
        )
        self.training_file_path:str = os.path.join(
            self.data_ingestion_dir,trainining_pipeline.DATA_INGESTION_INGESTED_DIR,trainining_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path:str = os.path.join(
            self.data_ingestion_dir,trainining_pipeline.DATA_INGESTION_INGESTED_DIR,trainining_pipeline.TEST_FILE_NAME
        )
        
        self.train_test_ration = trainining_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name = trainining_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = trainining_pipeline.DATA_INGESTION_DATABASE_NAME
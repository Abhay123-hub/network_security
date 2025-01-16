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


class ValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipeLineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,trainining_pipeline.DATA_VALIDATION_DIR_NAME)
        self.data_validation_valid_dir:str = os.path.join(self.data_validation_dir,trainining_pipeline.DATA_VALIDATION_VALID_DIR)
        self.data_validation_invlaid_dir:str = os.path.join(self.data_validation_dir,trainining_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.data_validation_valid_dir,trainining_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.data_validation_valid_dir,trainining_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.data_validation_invlaid_dir,trainining_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.data_validation_invlaid_dir,trainining_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(self.data_validation_dir,
                                                       trainining_pipeline.DATA_VALIDATION_DRTIFT_REPORT_DIR,
                                                       trainining_pipeline.DATA_VALIDATION_DRIFT_REPORT_NAME)
        
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipeLineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,trainining_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path = os.path.join(self.data_transformation_dir,trainining_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                trainining_pipeline.TRAIN_FILE_NAME.replace('csv','npy'))
        self.transformed_test_file_path = os.path.join(self.data_transformation_dir,trainining_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                trainining_pipeline.TEST_FILE_NAME.replace('csv','npy'))
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir,trainining_pipeline.DATA_TRANSFOMRATION_TRANSFORMED_OBJECT_DIR,
                                                         trainining_pipeline.PREPROCESSING_OBJECT_FILE_NAME)

        
from networksecurity.entity.config_entity import (TrainingPipeLineConfig,DataIngestionConfig,
                                                  ValidationConfig,DataTransformationConfig,ModelTrainerConfig)
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
import os,sys
from networksecurity.cloud.s3_syncer import S3Sync
from networksecurity.constants.trainining_pipeline import TRAINING_BUCKET_NAME

from networksecurity.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,
                                                    ModelTrainerArtifact)
class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline = TrainingPipeLineConfig()
            self.s3_sync = S3Sync()
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def data_ingestion(self) ->DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(self.training_pipeline) 
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def data_validation(self,data_ingestion_artifact:DataIngestionArtifact) ->DataValidationArtifact:
        try:
            data_validation_config = ValidationConfig(self.training_pipeline)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def data_transformation(self,data_validation_artifact:DataValidationArtifact) ->DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(self.training_pipeline)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def model_trainer(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline)
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    ## local artifact is going to s3 bucket
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline.artifact_dir,aws_bucket_url=aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    ## local final model is going to s3 bucket
    def sync_artifact_final_model_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline.model_dir,aws_bucket_url=aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.data_ingestion()
            data_validation_artifcat = self.data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.data_transformation(data_validation_artifact=data_validation_artifcat)
            model_trainer_artifact = self.model_trainer(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_artifact_final_model_to_s3()
            return model_trainer_artifact
          
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
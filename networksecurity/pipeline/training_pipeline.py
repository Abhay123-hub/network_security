from networksecurity.entity.config_entity import (TrainingPipeLineConfig,DataIngestionConfig,
                                                  ValidationConfig,DataTransformationConfig,ModelTrainerConfig)
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
import os,sys

from networksecurity.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,
                                                    ModelTrainerArtifact)
class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline = TrainingPipeLineConfig()
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
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.data_ingestion()
            data_validation_artifcat = self.data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.data_transformation(data_validation_artifact=data_validation_artifcat)
            model_trainer_artifact = self.model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
          
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
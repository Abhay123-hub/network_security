from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_data_path:str
    test_data_path:str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    validation_train_file_path:str
    validation_test_file_path:str
    invalid_train_file_path:str
    invlaid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class ClassificationMetricArtifcat:
    f1_score: float
    precision_score:float
    recall_score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:ClassificationMetricArtifcat
    test_metric_artifact:ClassificationMetricArtifcat


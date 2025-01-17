from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import numpy as np

import os
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from networksecurity.utils.main_utils.utils3 import save_numpy_array
from networksecurity.utils.main_utils.utils4 import save_object
from networksecurity.utils.main_utils.utils5 import load_object
from networksecurity.utils.main_utils.utils6 import load_array
from networksecurity.utils.main_utils.utils7 import evaluate_models


from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_metric
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import (DecisionTreeClassifier)
from sklearn.ensemble import (AdaBoostClassifier,GradientBoostingClassifier,
                              RandomForestClassifier)
import mlflow

import dagshub
dagshub.init(repo_owner='rajputjiabhay3002', repo_name='network_security', mlflow=True)




## now let us creating the model trainer class
class ModelTrainer:
   
        def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
            try:
                self.model_trainer_config = model_trainer_config            
                self.data_transformation_artifact=data_transformation_artifact
            except Exception as e:
             raise NetworkSecurityException(e,sys)
        
        def track_mlflow(self,best_model,ClassificationMetric):
            try:
                with mlflow.start_run():
                    f1_score = ClassificationMetric.f1_score
                    recall_score = ClassificationMetric.recall_score
                    precision_score = ClassificationMetric.precision_score

                    mlflow.log_metric("f1_score",f1_score)
                    mlflow.log_metric("recall_score",recall_score)
                    mlflow.log_metric("precision_score",precision_score)

                    mlflow.sklearn.log_model(best_model,"model")
            except Exception as e:
                raise NetworkSecurityException(e,sys)
        
        
        
        def train_model(self,x_train,y_train,x_test,y_test):
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,]
            }
            
              }
            
            report:dict = evaluate_models(x_train=x_train,
                                      y_train=y_train,
                                      x_test=x_test,
                                      y_test=y_test,
                                      params=params,
                                      models=models)
            ## so what actually this report contains in it
            ## in keys of this report there is macine learning model name
            ## and corresponding to each machine learning model, there is the accuracy which we got for that machine learning model

            ## i want to get maximum accuracy
           
            best_model_score = max(sorted(report.values()))
            best_model_name = list(report.keys())[list(report.values()).index(best_model_score)]
            
            best_model = models[best_model_name]
            ## so till here i have got my best model after doing a lot of experimentation
            ## now i am going to do prediction based on that best model
            y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)
            classification_train_metric = get_classification_metric(y_pred=y_train_pred,y_true=y_train)
            self.track_mlflow(best_model,classification_train_metric)
            classification_test_metric = get_classification_metric(y_pred=y_test_pred,y_true=y_test)
            self.track_mlflow(best_model,classification_test_metric)
            
            ## get the processer from data transformation pipleine
            processor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            save_object("final_model/model.pkl",best_model)

            Network_Model = NetworkModel(processor=processor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path,Network_Model)
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            return model_trainer_artifact


        
        def initiate_model_trainer(self):
            try:
                train_file_path = self.data_transformation_artifact.transformed_train_file_path
                test_file_path = self.data_transformation_artifact.transformed_test_file_path

                ## loading training array and testing array
                train_arr = load_array(train_file_path)
                test_arr = load_array(test_file_path)

                x_train,y_train,x_test,y_test = (
                    train_arr[:,:-1],
                    train_arr[:,-1],
                    test_arr[:,:-1],
                    test_arr[:,-1],
                )
                model_trainer_artifact = self.train_model(x_train=x_train,
                                                          y_train=y_train,
                                                          x_test=x_test,
                                                          y_test=y_test)
                return model_trainer_artifact


            except Exception as e:
                raise NetworkSecurityException(e,sys)
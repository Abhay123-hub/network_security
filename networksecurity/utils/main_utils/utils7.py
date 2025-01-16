import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV



## creating a function for evaluating the models
def evaluate_models(x_train,y_train,x_test,y_test,models,params):
    try:
        report = {} ## defining an empty dictionary
        for i in range(len(list(models.keys()))):
            model = list(models.values())[i] ## this is the actual model
            para = params[list(models.keys())[i]]
            gs = GridSearchCV(model,para,cv =3)
            gs.fit(x_train,y_train) ## for this particular model
            ## i am experimenting with all the different parameters whcih i have used 
            model.set_params(**gs.best_params_) ## picking the best ever parameters
            model.fit(x_train,y_train) ## based on those parameters training my model
            ## now doing prediction based on this model
            
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test_pred,y_test)
            report[list(models.keys())[i]] = test_model_score
        return report




    except Exception as e:
        raise NetworkSecurityException(e,sys)
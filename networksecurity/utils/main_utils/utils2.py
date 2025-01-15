import os,sys
import numpy as np
#import dill
import pickle
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import yaml

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
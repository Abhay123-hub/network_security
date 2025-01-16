import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle

def load_array(file_path:str) ->np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the {file_path} does not exist")
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
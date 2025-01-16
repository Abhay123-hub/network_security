import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle



def save_object(file_path:str,obj:object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file:
            pickle.dump(obj,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
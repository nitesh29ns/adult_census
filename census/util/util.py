import yaml
import os, sys
from census.exception import classificationException
from census.logger import lg
from census.constant import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CURRENT_TIME_STAMP, BUCKET_NAME
import dill
import numpy as np
import pandas as pd
import boto3



def upload_model_to_s3 (model_path: str):
    try:
        session = boto3.Session(
                  aws_access_key_id= AWS_ACCESS_KEY_ID,
                  aws_secret_access_key= AWS_SECRET_ACCESS_KEY,)

        
        model_file_name = os.path.basename(model_path)

        directoryname = CURRENT_TIME_STAMP
        KeyFileName = f"{directoryname}/{model_file_name}"

        s3 = session.resource('s3')
        s3.meta.client.upload_file(Filename= model_path , Bucket= BUCKET_NAME , Key=KeyFileName)

    
    except Exception as e:
        raise classificationException(e,sys) from e




def read_yaml_file(file_path:str) ->dict :
    try :
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise classificationException(e,sys) from e

## dill is used to store python object into file 
def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise classificationException(e,sys) from e


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise classificationException(e,sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise classificationException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise classificationException(e, sys) from e


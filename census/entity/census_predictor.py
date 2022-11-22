from census.exception import classificationException
from census.util.util import load_object
import os, sys
import pandas as pd

class CensusData:

    def __init__(self,
                 age : int,
                  workclass : str,
                  education : str,
                  occupation : str,
                  sex : str,
                  hours_per_week : int,
                  country : str
                  ):
        try:
            self.age = age
            self.workclass = " "+ workclass.lower()
            self.education = " "+ education.lower()
            self.occupation = " "+ occupation.lower()
            self.sex = " "+ sex.lower()
            self.hours_per_week = hours_per_week
            self.country = " "+ country.lower()
        except Exception as e:
            raise classificationException(e, sys) from e
    
    def get_input_data_as_dataframe(self):
        try:
            census_input_dict = self.get_data_as_dict()

            return pd.DataFrame(census_input_dict)
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_data_as_dict(self):
        try:
            input_data = {
                "age" : [self.age],
                "workclass" : [self.workclass],
                "education" : [self.education],
                "occupation" : [self.occupation],
                "sex" : [self.sex],
                "hours_per_week" : [self.hours_per_week],
                "country" : [self.country]
            }
            return input_data
        except Exception as e:
            raise classificationException(e, sys) from e

    
class CensusPredictor:
    def __init__(self, model_dir: str):
        try:
            self.model_path = model_dir
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_model_path(self):
        try:
            folder_name = self.model_path
            file_name = os.listdir(folder_name)[0]
            latest_model_path = os.path.join(folder_name, file_name)
            
            return latest_model_path
        except Exception as e:
            raise classificationException(e, sys) from e

    def predict(self,X):
        try:
            model_path = self.get_model_path()
            model = load_object(file_path = model_path)
            predicted_salary = model.predict(X)
            prediction = ""
            if predicted_salary == [1.]:
                prediction = "salary is greater then (>) 50k."
            else :
                prediction = "salary is less then or equal to (<=) 50k."


            return prediction
        except Exception as e:
            raise classificationException(e, sys) from e
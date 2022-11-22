from census.exception import classificationException
from census.logger import lg
from census.util.util import read_yaml_file
import os, sys
import importlib


MODEL_KEY = 'model'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAMS_KEY = 'params'
MAX_ITER = 'max_iter'
PENALTY = 'penalty'
SOLVER = 'solver'



class Model_training:
    def __init__ (self,model_config_path :str):
        try:
            self.model_config : dict = read_yaml_file(model_config_path)

            self.model_moduel = self.model_config[MODEL_KEY][MODULE_KEY]
            self.model_moduel_class = self.model_config[MODEL_KEY][CLASS_KEY]
            self.model_param = self.model_config[MODEL_KEY][PARAMS_KEY]
            self.param_max_iter = self.model_param[MAX_ITER]
            self.param_penalty = self.model_param[PENALTY]
            self.param_solver = self.model_param[SOLVER]
        except Exception as e:
            raise classificationException(e, sys) from e
    
    @staticmethod
    def import_model(module_name:str, class_name: str):
        try:
            # load the module, will raise ImportError if module cannot be loaded
            module = importlib.import_module(module_name)
            lg.info(f"Executing command: from {module} import {class_name}")
            # get the class, will raise AttributeError if class cannot be found
            class_ref = getattr(module, class_name)

            return class_ref
        except Exception as e:
            raise classificationException(e, sys) from e

    def trained_model(self,input_features , output_fetures):
        try:
            model = Model_training.import_model(module_name=self.model_moduel,
                                                class_name=self.model_moduel_class)
            tuned_model = model(max_iter=self.param_max_iter, 
                                penalty=self.param_penalty,
                                solver=self.param_solver)
            #clf(max_iters=self.param_max_iter, penalty=self.param_penalty, solver=self.param_solver)
            tuned_model.fit(input_features, output_fetures)

            return tuned_model
        except Exception as e:
            raise classificationException(e, sys) from e


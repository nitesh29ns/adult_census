from census.exception import classificationException
from census.logger import lg
from census.entity.config_entity import modelevaluationconfig
from census.entity.artifact_entity import DataTransformationArtifact ,ModelTrainerArtifact ,ModelEvaluationArtifact
from census.util.util import load_numpy_array_data, load_object
from sklearn.metrics import classification_report
import os, sys
import pandas as pd
import numpy as np


class Model_evaluation:
    def __init__ (self, model_evaluation_config: modelevaluationconfig, data_transformation_artifact : DataTransformationArtifact, model_trainer_artifact: ModelTrainerArtifact):
        try:
            lg.info(f"{'>>' * 30}Model evaluation log started.{'<<' * 30} ")

            self.model_evaluation_config = model_evaluation_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_test_dataset_and_trained_model (self):
        try:
            lg.info("loading transformed test dataset.")
            transformed_test_file_path = self.data_transformation_artifact.transfromed_test_file_path
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)

            lg.info(f"Splitting training and testing input and target feature")
            x_test, y_test = test_array[:,:-1],test_array[:,-1]

            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            lg.info(f"load train model {trained_model_file_path}.")
            trained_model_obj = load_object(file_path=trained_model_file_path)
            trained_model = trained_model_obj.trained_model_object

            return x_test, y_test, trained_model
        except Exception as e:
            raise classificationException(e, sys) from e

    def evaluate_model_on_test_dataset(self):
        try:
            model_accepted = False
            x_test, y_test, trained_model = self.get_test_dataset_and_trained_model()

            base_accuracy = self.model_trainer_artifact.base_accuracy
            
            model_accuarcy = trained_model.score(x_test, y_test)

            if model_accuarcy >= base_accuracy:
                model_accepted = True
            else:
                model_accepted = False
                raise ValueError("Accuracy is not accepted.")

            lg.info(f"train model is accepted? : {model_accepted}.")

            return model_accepted    
        except Exception as e:
            raise classificationException(e, sys) from e

    def evaluation_report (self):
        try:
            x_test, y_test, trained_model = self.get_test_dataset_and_trained_model()

            y_preds = trained_model.predict(x_test)

            report = classification_report(y_test, y_preds, output_dict=True)
            
            lg.info(f"evaluation report = {report}.")
            evaluation_report = pd.DataFrame(report)

            model_evaluation_dir = self.model_evaluation_config.model_evaluation_report_dir
            model_evauation_file_path = self.model_evaluation_config.model_evaluation_file_path
            
            os.makedirs(model_evaluation_dir, exist_ok=True)
            evaluation_report.to_csv(model_evauation_file_path)

            return model_evauation_file_path

        except Exception as e:
            raise classificationException(e, sys) from e
    
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            self.evaluate_model_on_test_dataset()
            self.evaluation_report()

            model_evalation_artifact = ModelEvaluationArtifact(
                model_evaluation_file_path=self.evaluation_report()
            )

            return model_evalation_artifact
        except Exception as e:
            raise classificationException(e, sys) from e

    def __del__(self):
        lg.info(f"{ '>>' * 30} model evaluation log is complete.{'<<' * 30}")
        



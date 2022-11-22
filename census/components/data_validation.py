from census.exception import classificationException
from census.logger import lg
from census.entity.artifact_entity import DataIngestArtifact, DataValidationArtifact
from census.entity.config_entity import datavalidationconfig
from census.util.util import read_yaml_file
from census.constant import *
import pandas as pd
import numpy as np
import os, sys
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.model_profile import Profile
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab


class DataValidation:
    def __init__(self,data_validation_config: datavalidationconfig,
        data_ingestion_artifact: DataIngestArtifact)->None :
        try:
            lg.info(f"{'='*20}Data validation log started.{'='*20} ")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise classificationException(e, sys) from e

    def is_train_test_file_exist(self):
        try:
            lg.info("checking is train and test data are available.")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist
            lg.info(f"Is train and test file exists ? {is_available}.")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"training file: {training_file} or testing file: {testing_file} is not present."

            return is_available

        except Exception as e:
            raise classificationException(e, sys) from e

    def get_train_test_data(self):
        try:
            train_data = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_data = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_data, test_data
        except Exception as e:
            raise classificationException(e,sys) from e

    def validate_dataset_with_schema(self):
        try:
            validation_status = False

            schema_file = read_yaml_file(self.data_validation_config.schema_file_path)

            train_data, test_data = self.get_train_test_data()

            train_data.rename({"hours-per-week": "hours_per_week"}, inplace=True, axis=1)
            test_data.rename({"hours-per-week": "hours_per_week"}, inplace=True, axis=1)
    
            # extract required columns from ingested data
            valid_train_data = pd.DataFrame(train_data[list(schema_file['columns'])])
            valid_test_data = pd.DataFrame(test_data[list(schema_file['columns'])])

            # data  file name
            file_name = 'valid_data.csv'

            # converting target values in to 0 and 1.
            valid_train_data[schema_file['target_columns']] = valid_train_data[schema_file['target_columns']].map({TARGET_VALUE_NO : 0 , TARGET_VALUE_YES : 1})
            valid_test_data[schema_file['target_columns']] = valid_test_data[schema_file['target_columns']].map({TARGET_VALUE_NO : 0 , TARGET_VALUE_YES : 1})

            # lower all the categorical columns values
            for feature in schema_file[CATEGORICAL_COLUMNS]:
                valid_train_data[feature] = valid_train_data[feature].str.lower()

            for feature in schema_file[CATEGORICAL_COLUMNS]:
                valid_test_data[feature] = valid_test_data[feature].str.lower()

            # save final training data
            valid_train_file_path = os.path.join(self.data_validation_config.vaild_train_dir,file_name)
            os.makedirs(self.data_validation_config.vaild_train_dir, exist_ok=True)
            lg.info(f"exporting valid_training data into file {valid_train_file_path}")
            valid_train_data.to_csv(valid_train_file_path, index=False)
            
            # save final test data
            valid_test_file_path = os.path.join(self.data_validation_config.valid_test_dir,file_name)
            os.makedirs(self.data_validation_config.valid_test_dir, exist_ok=True)
            lg.info(f"exporting valid_training data into file {valid_test_file_path}")
            valid_test_data.to_csv(valid_test_file_path, index=False)

            # check is our data is acording to our schema file 
            if True:
                len(valid_train_data.columns) == len(schema_file['columns_dtypes'].keys())
                len(valid_test_data.columns) == len(schema_file['columns_dtypes'].keys())
                
                valid_train_data.columns == schema_file['columns']
                valid_test_data.columns == schema_file['columns']
                
                train_categorical = [features for features in valid_train_data if valid_train_data[features].dtype == 'O']
                train_numerical = [features for features in valid_train_data if valid_train_data[features].dtype != 'O']
                
                train_categorical == schema_file['categorical_columns']
                train_numerical == schema_file['numerical_columns']

                test_categorical = [features for features in valid_test_data if valid_test_data[features].dtype == 'O']
                test_numerical = [features for features in valid_test_data if valid_test_data[features].dtype != 'O']

                validation_status = True
            else:
                validation_status = False
                raise classificationException(Exception ,sys)

            lg.info(f"validation status is {validation_status}.")

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                valid_train_file_path=valid_train_file_path,
                valid_test_file_path=valid_test_file_path,
                message = 'data validation perform sucessfully.'
            )
            lg.info(f"data validation artifact is {data_validation_artifact}.")
            return data_validation_artifact
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_and_save_data_drift_report(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])

            train_data, test_data = self.validate_dataset_with_schema().valid_train_file_path, self.validate_dataset_with_schema().valid_test_file_path
            
            train_data = pd.read_csv(train_data)
            test_data = pd.read_csv(test_data)

            dashboard.calculate(train_data, test_data)

            report_file_path = os.path.join(self.data_validation_config.report_file_path)
            #os.makedirs(report_file_path, exist_ok=True)

            dashboard.save(report_file_path)


        except Exception as e:
            raise classificationException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exist()
            self.validate_dataset_with_schema()
            self.get_and_save_data_drift_report()

            return self.validate_dataset_with_schema()
        except Exception as e:
            raise classificationException(e, sys) from e


    def __del__(self):
        lg.info(f"{'='*20} data validation log complete. {'='*20}\n\n")
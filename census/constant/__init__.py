import os 
import datetime

ROOT_DIR = os.getcwd()   

def get_current_time_stamp():
    return f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


CONFIG_DIR = 'yaml_config' 
CONFIG_FILE_NAME = 'config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

SCHEMA_FILE_NAME = 'schema.yaml'
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,SCHEMA_FILE_NAME)


CURRENT_TIME_STAMP = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

# data ingestion related variables
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion' # name of the folder inside arifact 
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATASET_DOWNLOAD_URL_KEY = 'dataset_download_url'
DATASET_FILE_NAME_KEY = 'dataset_file_name'
RAW_DATA_DIR_KEY = 'raw_data_dir'
TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
ZIP_FILE_NAME_KEY = 'zip_File_name'
INGESTED_DIR_KEY = 'ingested_dir'
INGESTED_TRAIN_DIR_KEY = 'ingested_train_dir'
INGESTED_TEST_DIR_KEY = 'ingested_test_dir'

# data validation related variables
DATA_VALIDATION_ARTIFACT_DIR = 'data_validation'
DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = 'schema_file_name'
DATA_VALIDATION_SCHEMA_DIR = 'schema_dir'
REPORT_FILE_PATH_KEY = 'report_file_path'
VALID_DATA_DIR_KEY = 'valid_data_dir'
VALID_TRAIN_DIR_KEY = 'valid_train_dir'
VALID_TEST_DIR_KEY = 'valid_test_dir'

# data transformation related variables
DATA_TRANSFORMATION_ARTIFACT_DIR = 'data_transformation'
DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = 'transformed_dir'
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DATA = 'transformed_train_dir'
DATA_TRANSFORMATION_TRASFORMED_TEST_DATA = 'transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSED_DIR = 'preprocessing_dir'
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME = 'preprocessed_object_file_name'

# schema file related variables
NUMERICAL_COLUMNS = 'numerical_columns'
CATEGORICAL_COLUMNS = 'categorical_columns'
TARGET_COLUMN_KEY = 'target_columns'

TARGET_VALUE_NO = ' <=50K'
TARGET_VALUE_YES = ' >50K'

#Training pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config" 
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


# model training related variables
MODEL_TRAINER_ARTIFACT_DIR_KEY = 'model_training'
MODEL_TRAINER_CONFIG_KEY = 'model_trainer_config'
TRAINED_MODEL_DIR_KEY = 'trained_model_dir'
TRAINED_MODEL_CONFIG_DIR = 'model_config_dir'
TRAINED_MODEL_CONFIG_FILE_NAME = 'model_config_file_name'
TRAINED_MODEL_FILE_NAME = 'model_file_name'
TRAINED_MODEL_BASE_ACCURACY = 'base_accuracy'

# model evaluation related variables
MODEL_EVALUATION_ARTIFACT_DIR_KEY = 'model_evaluation'
MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config'
MODEL_EVALUATION_REPORT_DIR_KEY = 'evaluation_report_dir'
MODEL_EVALUATION_REPORT_FILE_NAME = 'evaluation_report_file_name'

# s3 bucket credenticals
AWS_ACCESS_KEY_ID = 'AKIAVEALGMKYBU2EQ344'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'census-prediction-model'

# model pusher related variables
MODEL_PUSHER_CONFIG_KEY ='model_pusher_config'
MODEL_PUSHER_SAVED_MODEL_DIR = 'saved_model_dir'
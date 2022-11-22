from census.exception import classificationException
from census.logger import lg
from census.constant import *
from census.entity.config_entity import *
from census.util.util import read_yaml_file
import os, sys
from datetime import datetime


class configration:
    def __init__(self,
        config_file_path:str = CONFIG_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP)->None :
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_data_ingestion_config(self)->dataingestionconfig: # dataingestionconfig just for the documentation purposes.
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )

            os.makedirs(data_ingestion_artifact_dir, exist_ok=True)

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATASET_DOWNLOAD_URL_KEY]

            dataset_file_name = data_ingestion_info[DATASET_FILE_NAME_KEY]


            tgz_download_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[TGZ_DOWNLOAD_DIR_KEY])

            zip_file_name = data_ingestion_info[ZIP_FILE_NAME_KEY]

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[RAW_DATA_DIR_KEY])

            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[INGESTED_DIR_KEY])

            ingested_train_dir = os.path.join(data_ingestion_artifact_dir,
            ingested_data_dir,
            data_ingestion_info[INGESTED_TRAIN_DIR_KEY])

            ingested_test_dir = os.path.join(data_ingestion_artifact_dir,
            ingested_data_dir,
            data_ingestion_info[INGESTED_TEST_DIR_KEY])

            data_ingestion_config = dataingestionconfig(
                dataset_download_url=dataset_download_url,
                dataset_file_name=dataset_file_name,
                tgz_download_dir=tgz_download_dir,
                zip_File_name=zip_file_name,
                raw_data_dir=raw_data_dir,
                ingested_dir=ingested_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )
            lg.info(f"data ingestion config: [{data_ingestion_config}].")
            return data_ingestion_config

        except Exception as e:
            raise classificationException(e, sys) from e

    def get_data_validation_config(self)-> datavalidationconfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir = os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR,
                self.time_stamp
            )

            data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(ROOT_DIR,
                data_validation_info[DATA_VALIDATION_SCHEMA_DIR],
                data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            valid_data_dir = os.path.join(
                data_validation_artifact_dir,
                data_validation_info[VALID_DATA_DIR_KEY]
            )

            valid_train_data_dir = os.path.join(
                valid_data_dir,
                data_validation_info[VALID_TRAIN_DIR_KEY]
            )

            valid_test_data_dir = os.path.join(
                valid_data_dir,
                data_validation_info[VALID_TEST_DIR_KEY]
            )

            report_file_path = os.path.join(
                data_validation_artifact_dir,
                data_validation_info[REPORT_FILE_PATH_KEY]
            )
            
            data_validation_config = datavalidationconfig(
                schema_file_path= schema_file_path,
                report_file_path= report_file_path,
                valid_data_dir= valid_data_dir,
                vaild_train_dir= valid_train_data_dir,
                valid_test_dir= valid_test_data_dir
            )

            lg.info(f"data validation config {data_validation_config}.")
            return data_validation_config

        except Exception as e:
            raise classificationException(e, sys) from e

    def get_data_transformation_config(self):
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir


            data_transformation_artifact = os.path.join(
                artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_DIR,
                self.time_stamp
            )

            data_transformation_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            transformed_data_dir = os.path.join(
                data_transformation_artifact,
                data_transformation_info[DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR]
            )

            transformed_train_data_dir = os.path.join(
                transformed_data_dir,
                data_transformation_info[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DATA]
            )

            transformed_test_data_dir = os.path.join(
                transformed_data_dir,
                data_transformation_info[DATA_TRANSFORMATION_TRASFORMED_TEST_DATA]
            )

            preprocessing_dir = os.path.join(
                data_transformation_artifact,
                data_transformation_info[DATA_TRANSFORMATION_PREPROCESSED_DIR]
            )

            preprocessing_file_object = os.path.join(preprocessing_dir,data_transformation_info[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME])

            data_transformation_config = datatransformationconfig(
                transformed_train_dir=transformed_train_data_dir,
                transformed_test_dir= transformed_test_data_dir,
                preprocessing_object_file_path= preprocessing_file_object
            )

            return data_transformation_config

        except Exception as e:
            raise classificationException(e, sys) from e

    def get_model_trainer_config(self)-> modeltrainerconfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            model_trainer_config = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            model_trainer_artifact = os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR_KEY,
                self.time_stamp
                )

            trained_model_file_path = os.path.join(
                model_trainer_artifact,
                model_trainer_config[TRAINED_MODEL_DIR_KEY],
                model_trainer_config[TRAINED_MODEL_FILE_NAME]
            )

            base_accuracy = model_trainer_config[TRAINED_MODEL_BASE_ACCURACY]

            trained_model_config_file_path = os.path.join(
                model_trainer_config[TRAINED_MODEL_CONFIG_DIR],
                model_trainer_config[TRAINED_MODEL_CONFIG_FILE_NAME]
            )

            trained_model_config = modeltrainerconfig(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_config_file_path=trained_model_config_file_path
            )
            
            return trained_model_config
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_model_evaluation_config(self)-> modelevaluationconfig:
        try:
            artifact = self.training_pipeline_config.artifact_dir

            model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]

            model_evaluation_artifact = os.path.join(
                artifact,
                MODEL_EVALUATION_ARTIFACT_DIR_KEY,
                self.time_stamp
            )

            model_evaluation_report_dir = os.path.join(
                model_evaluation_artifact,
                model_evaluation_config[MODEL_EVALUATION_REPORT_DIR_KEY]
            )
            
            model_evaluation_report_file_path = os.path.join(model_evaluation_report_dir, model_evaluation_config[MODEL_EVALUATION_REPORT_FILE_NAME])
            
            model_evaluation_config = modelevaluationconfig(
                model_evaluation_report_dir=model_evaluation_report_dir,
                model_evaluation_file_path=model_evaluation_report_file_path
            )

            return model_evaluation_config

        except Exception as e:
            raise classificationException(e, sys) from e

    def get_model_pusher_config(self)-> modelPusherconfig:
        try:
            model_pusher_config = self.config_info[MODEL_PUSHER_CONFIG_KEY]

            saved_model_path = os.path.join(ROOT_DIR,model_pusher_config[MODEL_PUSHER_SAVED_MODEL_DIR])

            model_pusher_config = modelPusherconfig(
                saved_model_path=saved_model_path)

            return model_pusher_config
        
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_training_pipeline_config(self)-> trainingpipelineconfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])

            os.makedirs(artifact_dir, exist_ok=True)

            training_pipeline_config = trainingpipelineconfig(artifact_dir = artifact_dir)
            lg.info(f"training pipeline config: [{training_pipeline_config}]")
            return training_pipeline_config
        except Exception as e:
            raise classificationException(e, sys) from e
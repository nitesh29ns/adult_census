from census.exception import classificationException
from census.logger import lg
from census.entity.artifact_entity import *
from census.entity.config_entity import modelPusherconfig
from census.constant import *
from census.util.util import upload_model_to_s3
import os, sys
import boto3


class Model_Pusher:
    def __init__(self,model_pusher_config : modelPusherconfig, 
                model_trainer_artfact: ModelTrainerArtifact):
        try:
            lg.info(f"{'>>' * 30} model pusher log stared. {'<<' * 30}")
            self.model_pusher_config = model_pusher_config
            self.model_trainer_artfact = model_trainer_artfact
        except Exception as e:
            raise classificationException(e, sys) from e
    
    def export_model_to_bucket(self):
        try:
            model_path = self.model_trainer_artfact.trained_model_file_path
        
            trained_model = upload_model_to_s3(model_path=model_path)
            lg.info(f"model upload to s3 bucket .")
            
        except Exception as e:
            raise classificationException(e, sys) from e
    
    def import_model(self):
        try:
            model_path = self.model_trainer_artfact.trained_model_file_path

            model_name = os.path.basename(model_path)
            FileName = f"{CURRENT_TIME_STAMP}/{model_name}"

            session = boto3.Session(
                  aws_access_key_id= AWS_ACCESS_KEY_ID,
                  aws_secret_access_key= AWS_SECRET_ACCESS_KEY,)

            os.makedirs(self.model_pusher_config.saved_model_path, exist_ok=True)

            saved_model_path = os.path.join(self.model_pusher_config.saved_model_path,model_name)

            s3 = session.resource('s3')
            s3.meta.client.download_file(BUCKET_NAME, FileName, saved_model_path)
            lg.info("download model from the s3 bucket at {saved_model_path}")

            return saved_model_path
        except Exception as e:
            raise classificationException(e, sys) from e

    def initiate_model_pusher(self)-> ModelPusherArtifact:
        try:
            self.export_model_to_bucket()
            self.import_model()
            model_pusher_artifact = ModelPusherArtifact(
                is_model_pusher=True,
                export_model_file_path=self.import_model()
            )
            
            return model_pusher_artifact

        except Exception as e:
            raise classificationException(e, sys) from e

    def __del__(self):
        lg.info(f"{'>>' * 30} model pusher log completed. {'<<' * 30}")
        
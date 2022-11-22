from census.exception import classificationException
from census.logger import lg
from census.entity.artifact_entity import *
import os , sys
from census.components.data_ingestion import DataIngestion
from census.components.data_validation import DataValidation
from census.components.data_transformation import DataTransformation
from census.components.model_trainer import Model_trainer
from census.components.model_evaluation import Model_evaluation
from census.components.model_pusher import Model_Pusher
from census.config.configuration import configration
from threading import Thread




class Pipeline(Thread) :

    def __init__(self, config:configration)-> None:
        try :
            os.makedirs(config.training_pipeline_config.artifact_dir, exist_ok=True)
            self.config = config
        except Exception as e :
            raise classificationException(e, sys) from e

    def start_data_ingestion(self)-> DataIngestArtifact:
        try :
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())

            return data_ingestion.initiate_data_ingestion()


        except Exception as e :
            raise classificationException(e, sys) from e

    def start_data_validation(self,data_ingestion_artfact = DataIngestArtifact)-> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                            data_ingestion_artifact=data_ingestion_artfact)

            return data_validation.initiate_data_validation()
        except Exception as e:
            raise classificationException(e, sys) from e

    def start_data_transformation(self,data_validation_artifact = DataValidationArtifact)-> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),
                                                    data_validation_artifact=data_validation_artifact)

            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise classificationException(e, sys) from e
    
    def start_model_trainer(self,data_transformation_artifact=DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = Model_trainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact)

            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise classificationException(e, sys) from e

    def start_model_evaluation(self,data_transformation_artifact = DataTransformationArtifact,
                               model_trainer_artifact = ModelTrainerArtifact)-> ModelEvaluationArtifact:
        try:
            model_evaluation = Model_evaluation(model_evaluation_config=self.config.get_model_evaluation_config(),
                                                data_transformation_artifact=data_transformation_artifact,
                                                model_trainer_artifact=model_trainer_artifact)

            return model_evaluation.initiate_model_evaluation()
        except Exception as e:
            raise classificationException(e, sys) from e
    
    def start_model_pusher(self,model_trainer_artifact = ModelTrainerArtifact) -> ModelPusherArtifact:
        try:
            model_pusher = Model_Pusher(model_pusher_config= self.config.get_model_pusher_config(),
                                        model_trainer_artfact=model_trainer_artifact)

            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise classificationException(e, sys) from e

        





    def run_pipeline(self):
        try:
            lg.info("pipeline starting.")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artfact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_transformation_artifact=data_transformation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)

            model_pusher_artifact = self.start_model_pusher(model_trainer_artifact=model_trainer_artifact)
        
            return model_pusher_artifact 

        except Exception as e:
            raise classificationException(e, sys) from e

    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise e 

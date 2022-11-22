from census.exception import classificationException
from census.logger import lg
from census.entity.config_entity import modeltrainerconfig
from census.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from census.entity.model_factory import Model_training
from census.util.util import load_numpy_array_data , load_object, save_object
import os , sys




class ClassifactionEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class Model_trainer:
    def __init__(self, model_trainer_config : modeltrainerconfig, data_transformation_artifact : DataTransformationArtifact):
        try:
            lg.info(f"{'>>' * 30}Model trainer log started.{'<<' * 30} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise classificationException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            lg.info("loading transformed train dataset.")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array_data(file_path=transformed_train_file_path)

            lg.info("loading transformed test dataset.")
            transformed_test_file_path = self.data_transformation_artifact.transfromed_test_file_path
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)

            lg.info(f"Splitting training and testing input and target feature")
            x_train,y_train,x_test,y_test = train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]

            lg.info(f"Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            lg.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory = Model_training(model_config_path=model_config_file_path)

            trained_model = model_factory.trained_model(input_features=x_train, output_fetures=y_train)
            lg.info(f"model is trained in train dataset: {trained_model}")

            preprocessing_obj=  load_object(file_path=self.data_transformation_artifact.preprocessing_object_file_path)

            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            census_model = ClassifactionEstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=trained_model)
            lg.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=census_model)

            base_accuracy = self.model_trainer_config.base_accuracy

            model_trainer_artifact = ModelTrainerArtifact(
                message= 'model training successfully.',
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy
            )

            lg.info(f"model trainer artifact {model_trainer_artifact}.")
            
            return model_trainer_artifact
        except Exception as e:
            raise ClassifactionEstimatorModel(e, sys) from e

    def __del__(self):
        lg.info(f"{'>>' * 30}Model trainer log completed.{'<<' * 30} ")


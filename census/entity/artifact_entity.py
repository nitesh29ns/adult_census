from collections import namedtuple

DataIngestArtifact = namedtuple('DataIngestArtifact',
['train_file_path','test_file_path','message'])

DataValidationArtifact = namedtuple('DataValidationArtifact',
['schema_file_path','report_file_path','valid_train_file_path','valid_test_file_path','message'])

DataTransformationArtifact = namedtuple('DataTransformationArtifact',
['transformed_train_file_path','transfromed_test_file_path','preprocessing_object_file_path','message'])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", [ "message", "trained_model_file_path","base_accuracy"])

ModelEvaluationArtifact = namedtuple('ModelEvaluationArtifact',['model_evaluation_file_path'])

ModelPusherArtifact = namedtuple("ModelPusherArtifact", ["is_model_pusher", "export_model_file_path"])

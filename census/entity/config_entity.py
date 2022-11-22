from collections import namedtuple

dataingestionconfig = namedtuple('dataingestionconfig',
['dataset_download_url','dataset_file_name','raw_data_dir','tgz_download_dir','zip_File_name','ingested_dir','ingested_train_dir','ingested_test_dir'])

datavalidationconfig = namedtuple('datavalidationconfig',
['schema_file_path','report_file_path','valid_data_dir','vaild_train_dir','valid_test_dir'])

datatransformationconfig = namedtuple('datatransformationconfig',
['transformed_train_dir','transformed_test_dir','preprocessing_object_file_path'])


modeltrainerconfig = namedtuple("modelTrainerconfig",["trained_model_file_path","base_accuracy","model_config_file_path"])

modelevaluationconfig = namedtuple("modelevaluationconfig",['model_evaluation_report_dir','model_evaluation_file_path'])

modelPusherconfig = namedtuple("modelPusherconfig",["saved_model_path"])




trainingpipelineconfig = namedtuple('trainingpipelineconfig',
['artifact_dir'])

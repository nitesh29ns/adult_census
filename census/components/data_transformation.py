from census.exception import classificationException
from census.logger import lg
from census.config.configuration import configration
from census.util.util import save_object, read_yaml_file, save_numpy_array_data
from census.entity.artifact_entity import *
from census.entity.config_entity import datatransformationconfig
from census.constant import *
import pandas as pd
import numpy as np
import os, sys
from sklearn.pipeline import Pipeline
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer




class DataTransformation:
    def __init__(self,data_transformation_config : datatransformationconfig,
        data_validation_artifact : DataValidationArtifact):
        try:
            lg.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise classificationException(e, sys) from e

    def get_data_transformation_object(self)->ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMNS]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMNS]

            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy="median")),
                ('scaler',StandardScaler())
            ])

            cat_pipeline =  Pipeline(steps=[
                ('imputer', SimpleImputer(strategy="most_frequent")),
                ('one_hot_encoder', OneHotEncoder()),
                ('scaline',StandardScaler(with_mean=False))
                ])

            lg.info(f"categorical columns: {categorical_columns}")
            lg.info(f"Numerical columns: {numerical_columns}")

            preprocessing_object = ColumnTransformer(transformers=[
                        ('num_pipeline',num_pipeline,numerical_columns),
                        ('cat_pipeline',cat_pipeline,categorical_columns)
                        ])
            return preprocessing_object

        except Exception as e:
            raise classificationException(e, sys) from e

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            lg.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformation_object()

            lg.info(f"Obtaining training and test file path.")
            train_file_path = self.data_validation_artifact.valid_train_file_path
            test_file_path = self.data_validation_artifact.valid_test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            lg.info(f"Loading training and test data as pandas dataframe.")

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]

            lg.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            lg.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            train_arr = np.c_[input_feature_train_arr.toarray(), np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr.toarray(), np.array(target_feature_test_df)]
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            lg.info(f"Saving transformed training and testing array.")
            
            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessing_object_file_path

            lg.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=transformed_train_file_path,
                transfromed_test_file_path=transformed_test_file_path,
                preprocessing_object_file_path=preprocessing_obj_file_path,
                message="Data transformation successfull."
            )
            lg.info(f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise classificationException(e, sys) from e
 
    def __del__(self):
        lg.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")

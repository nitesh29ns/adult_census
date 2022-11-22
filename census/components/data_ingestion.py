from census.exception import classificationException
from census.logger import lg
from census.entity.config_entity import dataingestionconfig
from census.entity.artifact_entity import DataIngestArtifact
from census.constant import *
import pandas as pd
import numpy as np
import zipfile
import os, sys
from sklearn.model_selection import StratifiedShuffleSplit
from kaggle.api.kaggle_api_extended import  KaggleApi



class DataIngestion:

    def __init__(self,data_ingestion_config:dataingestionconfig):
        try:
            lg.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise classificationException(e,sys) from e

    def download_dataset(self)->str:
        try:
            # dataset url
            download_url = self.data_ingestion_config.dataset_download_url
            file_name = self.data_ingestion_config.dataset_file_name
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            # to remove the tgz folder if exists 
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
            
            # to make the tgz folder 
            os.makedirs(tgz_download_dir, exist_ok=True)
            

            lg.info(f"downloding file from [{download_url}] into [{tgz_download_dir}].")
            # extract tgz file using kaggle api
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_file(download_url,
                                      file_name=file_name,path=tgz_download_dir)
            lg.info(f"[{tgz_download_dir}] is downloaded sucessfully using kaggle api.")
            return tgz_download_dir
        except Exception as e:
            raise classificationException(e,sys) from e

    def extract_tgz_file(self,tgz_dir:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            zip_file = os.path.join(tgz_dir,
            self.data_ingestion_config.zip_File_name)

            lg.info(f"extract tgz_file[{zip_file}] into [{raw_data_dir}].")
            with zipfile.ZipFile(zip_file) as census_tgz_file_obj:
                census_tgz_file_obj.extractall(path=raw_data_dir)

            lg.info(f"extraction completed.")
        except Exception as e:
            raise classificationException(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            census_file_path = os.path.join(raw_data_dir, file_name)

            lg.info(f"read csv file[{file_name}]")
            census_dataset = pd.read_csv(census_file_path)
            x = census_dataset.drop(columns='salary')
            y = census_dataset['salary']

            lg.info(f"split data in to train and test.")
            train_dataset = None
            test_dataset = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=42)

            for train_index, test_index in split.split(x,y):
                train_dataset = census_dataset.iloc[train_index]
                test_dataset = census_dataset.iloc[test_index]

            train_file_path  = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            if train_dataset is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                lg.info(f"exporting train dataset into file [{train_file_path}]")
                train_dataset.to_csv(train_file_path, index=False)

            if test_dataset is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                lg.info(f"exporting test dataset to file [{test_file_path}]")
                test_dataset.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestArtifact(train_file_path=train_file_path,
                                                         test_file_path=test_file_path,
                                                         message=f"data ingestion completed sucessfully.")

            lg.info(f"data ingestion artifact [{data_ingestion_artifact}]")
            return data_ingestion_artifact
            
        except Exception as e:
            raise classificationException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestArtifact:
        try:
            tgz_file_path = self.download_dataset()
            self.extract_tgz_file(tgz_dir=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise classificationException(e, sys) from e


    def __del__(self):
        lg.info(f"{'='*20} data ingestion log complete. {'='*20}\n\n")


from census.exception import classificationException
from census.logger import lg
from census.pipeline.pipeline import Pipeline
from census.config.configuration import configration
from census.components.data_ingestion import DataIngestion
from census.config.configuration import configration
from census.constant import *
import os, sys

def main():
    try:
        pipeline = Pipeline(config=configration(current_time_stamp=get_current_time_stamp()))
        pipeline.run()
        lg.info("main funcation ececuted completed.")
    except Exception as e :
        lg.error(f"{e}")
        print(e)


if __name__ =="__main__":
    main()
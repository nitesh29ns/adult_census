import streamlit as st
import altair as alt
from census.exception import classificationException
from census.logger import lg
from census.pipeline.pipeline import Pipeline
from census.config.configuration import configration
from census.components.data_ingestion import DataIngestion
from census.config.configuration import configration
from census.constant import *
from census.entity.census_predictor import CensusData, CensusPredictor
import webbrowser

import os, sys



SAVED_MODELS_DIR_NAME = "saved_model"
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


def predict(age,workclass,education,occupation,sex,hours_per_week,country):
    census_data = CensusData(age=age,
                                workclass=workclass,
                                education=education,
                                occupation=occupation,
                                sex=sex,
                                hours_per_week=hours_per_week,
                                country=country)
    
    census_df = census_data.get_input_data_as_dataframe()
    census_predictor = CensusPredictor(model_dir=MODEL_DIR)
    predicted_value = census_predictor.predict(X=census_df)

    return predicted_value


def start_pipeline():
    try:
        pipeline = Pipeline(config=configration(current_time_stamp=get_current_time_stamp()))
        pipeline.run()
    except Exception as e:
        raise classificationException(e, sys)



work = ["local-gov", "private", "self-emp-not-inc","state-gov","self-emp-inc","federal-gov","never-worked","without-pay","?"]
occ_input = ["craft-repair","exec-managerial","prof-specialty","adm-clerical","sales","machine-op-inspct","transport-moving","handlers-cleaners","farming-fishing","tech-support","protective-serv","priv-house-serv","armed-forces","other-service","?"]
edu_input = [ "HS-grad",
            "Some-college",  
            "Bachelors",      
            "Masters",          
            "Assoc-voc",        
            "11th",             
            "Assoc-acdm",       
            "10th",             
            "7th-8th",           
            "Prof-school",       
            "9th",               
            "12th",              
            "Doctorate",         
            "5th-6th",          
            "1st-4th",           
            "Preschool"]



def main():
    
    st.set_page_config(layout="wide")

    with st.sidebar:
        st.header("About")
        st.write("""
                My Name is Nitesh Sharma and This is my Intership project under ineuron Intership.
                ***
                github :- https://github.com/nitesh29ns/adult_census
                 
                linkdin :- https://www.linkedin.com/in/nitesh-sharma-0a260b183/
                """)

    with st.container():

        st.title("Salary Predictor")
        st.write("""
            This app predict whether your Salary is Greater than 50K or Less Then 50K.
            ***
            """)

        with st.expander("Initiate ML Pipeline..."):
            result = ""
            if st.button("Start Pipeline"):
                start_pipeline()
                result = "ML Pipeline Completed Successfully."
            st.success(result)

        html_temp = """
        <div style="background-color:tomato;padding:5px">
        <h2 style="color:white;text-align:center;">Salary Predictor ML App </h2>
        </div>
        """

        st.markdown(html_temp,unsafe_allow_html=True)

        age = st.slider("age",min_value=16, max_value=90)
        workclass = st.selectbox("workclass",work)
        education = st.selectbox("education",edu_input)
        occupation = st.selectbox("occupation",occ_input)
        sex = st.radio("sex", ["Male","Female"])
        hours_per_week = st.number_input("hours_per_week")
        country = st.text_input("country", "Type Here")
        
        result = ""
        if st.button("Predict"):
            result=predict(age=age,
                        workclass=workclass,
                        education=education,
                        occupation=occupation,
                        sex=sex,
                        hours_per_week=hours_per_week,
                        country=country)
        st.success(result)


if __name__ == "__main__":
    main()
from setuptools import setup, find_packages
from typing import List

#declaring variables for setup funcations
PROJECT_NAME= "census-predictor"
VERSION="0.0.1"
AUTHOR="Nitesh Sharma"
DESCRIPTION="This is a adult census prediction model"
REQUIREMENT_FILE_NAME="requirements.txt"


def get_requirements_list()->List[str]: # List[str] used to declare the structure of the output.
    """
    description : this funcation is going to return the list of requirements mention in the requirements.txt file

    return_type :List[str]
    """
    with open(REQUIREMENT_FILE_NAME) as requirements_file:
        return requirements_file.readlines().remove("-e .") 
          
          
# .remove("-e .") beacuse we use find_packages()


setup(
name =PROJECT_NAME,
version =VERSION,
author =AUTHOR,
description =DESCRIPTION,
packages =find_packages(),  #read code we write in the __init__.py, where it has __init__.py it read the file, -e . is eaual to find_pakages()
install_requires =get_requirements_list()
)

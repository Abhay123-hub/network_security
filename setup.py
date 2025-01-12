""""  the setup.py file is an essential part of pacakging and distributing python projects.
It is used by setup tools to define the configuration for your project such as its metadata
, dependencies and more

            """

from setuptools import find_packages,setup
from typing import List

def get_requirements() ->List[str]:
    """ This function will return a list of requirements
             """
    requirements_list:List[str] = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip() ## removing the blank space from the line and only collecting the requirement
                ## ignore empty line and -e .
                if requirement and requirement !="-e .":
                    requirements_list.append(requirement)
            return requirements_list
    except FileNotFoundError:
        print("file requirements.txt not found")
print(get_requirements())


setup(
    name = "Network Security",
    version = "0.0.1",
    author = "Abhay Thakur",
    author_email = "rajputjiabhay3002@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)



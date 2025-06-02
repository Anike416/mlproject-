from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    'this function returns a list of requirements from a file'
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[r.replace('\n','')for r in requirements]
    
        if '-e.' in requirements:
            requirements.remove('-e.')
            
    return requirements

setup(
    name='mlproject',
    version='0.0.1',
    author='Aniket',
    author_email='nainwal005@kgpian.iitkgp.ac.in',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
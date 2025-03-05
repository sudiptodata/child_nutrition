from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    Read requirements from specified file
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]
        
        # Remove empty lines and editable install marker
        requirements = [req for req in requirements if req and req != "-e ."]
        
    return requirements

setup(
    name='health_intervention_predictor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),  # Fixed with quotes
    entry_points={
        'console_scripts': [
            'health-intervention-predict=health_model.cli:main',
        ],
    },
    author='Sudipto K Mahato',
    author_email='sudiptokumarmahato@gmail.com',
    description='Predictive model for health intervention prioritization',
    url='https://github.com/yourusername/health-intervention-predictor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
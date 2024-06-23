
from setuptools import setup, find_packages

setup(
    name='OpticalElement',
    version='0.0.1',
    author='reround',
    author_email='ysz060625@gmail.com',
    description='Same of Optical Element',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'pandas>=1.0.0'
    ]
)
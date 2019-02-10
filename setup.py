from setuptools import setup, find_packages

setup(name='TV Series Details', 
version='1.0',
description='Package that will allow you to create useful and interesting graphs from tv sereis data',
author='Jakub Pilch',
install_requires=['bokeh', 'imdbpy'],
license="MIT",
packages=find_packages())
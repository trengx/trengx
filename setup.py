# python setup.py sdist bdist_wheel
# pip install twine
# twine upload dist/*
# username: jun-trengx
# password: B******9

from setuptools import setup, find_packages

setup(
    name='trengx',
    version='0.0.5',
    author='Yong-Jun Shin',
    packages=find_packages(),
    install_requires=[
    ],
)

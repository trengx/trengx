# python setup.py sdist bdist_wheel
# pip install twine
# twine upload dist/*
# username: jun-************
# password: B*************

from setuptools import setup, find_packages

setup(
    name='trengx',
    version='0.0.13',
    author='Yong-Jun Shin @trengx',
    packages=find_packages(),
    install_requires=[
    ],
)

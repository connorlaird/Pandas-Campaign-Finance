#!/usr/bin/env python

from distutils.core import setup

setup(
    name='PandasCampaignFinance',
    version='0.0.1',
    author="Connor Laird",
    author_email="connorlaird@gmail.com",
    py_modules=["PandasCampaignFinance"],
    url="https://github.com/connorlaird/Pandas-Campaign-Finance",
    description="Python wrapper to generate pandas DataFrames from the New York Times' Campaign Finance API.",
    requires=["pandas"],
    long_description=open('README.md').read(),
    classifiers=[
    ],
)
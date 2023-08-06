from setuptools import setup

"""
Steps to create a package: 
1. python setup.py sdist bdist_wheel
2. twine upload dist/*
    a. insert username and password and you're good. 
"""

classifiers = [
    #'DEVELOPMENT STATUS :: 2 - PRE-ALPHA',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mobility_graph',
    version='0.0.2',
    description='This package reads gtfs data and returns data of type dict',
    Long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'mobility-graph': 'mobility_graph', },
    packages=['mobility_graph'],
    url='',
    author='Ayman Mahmoud',
    author_email='aymanh.abdelhamid@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords=['gtfs', 'transit','mobility'],
    install_requires=['networkx', 'matplotlib'],
    extras_require = {
        "dev": [
          "pytest>=3.7",
        ],
    }
)

import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="fiftyone_location",
    version="4.0.0",
    author="51Degrees",
    url="http://51degrees.com/",
    description=("The 51Degrees Pipeline API is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines). "
    "This repository contains the geo-location engines for the Python implementation of the Pipeline API."),
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=2.7',
    packages=["fiftyone_location"],
    install_requires=["fiftyone_pipeline_core", "fiftyone_pipeline_engines", "fiftyone_pipeline_cloudrequestengine"],
    license="EUPL-1.2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    include_package_data=True
)

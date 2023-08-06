import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="fiftyone_pipeline_cloudrequestengine",
    version="4.0.0",
    author="51Degrees",
    url="http://51degrees.com/",
    description=("The 51Degrees Pipeline API is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines). "
    "This package extends the flow element class created by the fiftyone.pipeline.core pacakge into a specialized type of flow element called an engine."),
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=2.7',
    packages=["fiftyone_pipeline_cloudrequestengine"],
    install_requires=[
          'requests',
    ],
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

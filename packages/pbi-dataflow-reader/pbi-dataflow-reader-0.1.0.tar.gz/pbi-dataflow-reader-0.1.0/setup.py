import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pbi-dataflow-reader",
    version="0.1.0",
    description="Python client library to access data from PowerBI dataflow",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/allenwux/powerbi-datasource",
    author="Xiaochen Wu",
    author_email="xiwu@microsoft.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["dataflow"],
    include_package_data=True,
    install_requires=["azure-storage-blob", "pandas"],
    entry_points={},
)
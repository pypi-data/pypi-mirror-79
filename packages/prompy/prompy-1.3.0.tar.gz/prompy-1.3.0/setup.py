import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="prompy",
    version="1.3.0",
    description="prompy",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    author="Dominique Sommers",
    author_email="dominiquesommers88@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["prompy"],
    include_package_data=True
)

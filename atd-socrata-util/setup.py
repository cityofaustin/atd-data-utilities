import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atd-socrata-util",
    version="0.0.6",
    author="City of Austin",
    author_email="transportation.data@austintexas.gov",
    description="Utilities interacting with the Socrata Open Data API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-socrata-util",
    install_requires = [
        "requests",
        "atd-data-util"
    ],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta", 
    ),
)


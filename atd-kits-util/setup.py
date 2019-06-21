import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atd-kits-util",
    version="0.0.2",
    author="City of Austin",
    author_email="transportation.data@austintexas.gov",
    description="Python utilities for interacting with KITS, an advanced transportation management application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-kits-util",
    install_requires = [
        "arrow",
        "pymssql"
    ],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta", 
    ),
)


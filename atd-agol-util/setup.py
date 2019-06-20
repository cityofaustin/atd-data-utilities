import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atd-agol-util",
    version="0.0.5",
    author="City of Austin",
    author_email="transportation.data@austintexas.gov",
    description="Python utilities interacting with the ArcGIS Online (AGOL) API.",
    install_requires=[
      'requests',
      'arcgis',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-agol-util",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ),
)
# Austin Transportation Python Utilities

This is the transportation department utilities repository, it contains development and integration tools for different applications and platforms utilized by the department. The packages follow a monorepo architecture to keep our tools centralized, and this structure allows us to easily maintain these tools and keep a single pipeline for automated deployments for general use in pipy.org.

## Packages

These are the packages that are contained within this repository:

- [atd-email-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-email-util)
- [atd-data-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-data-util)
- [atd-args-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-args-util)
- [atd-jobs-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-jobs-util)
- [atd-log-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-log-util)
- [atd-knack-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-knack-util)
- [atd-agol-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-agol-util)
- [atd-socrata-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-socrata-util)
- [atd-kits-util](https://github.com/cityofaustin/atd-data-utilities/tree/master/atd-kits-util)
## CD/CI

We make use of CircleCI for our deployments, you can see the build script in the `.circleci` folder in this repo. The basic process consists of a couple steps:

1. First, the script will gather information from `.circleci/packages.json` to determine what packages need to be looked at. This file contains a list of the packages we need to deploy automatically, in other words, if the package is not listed here, the deployment script will not pay attention to it. The string is the exact name of the folder where the package's `setup.py` file and source code live.
2. The script will iterate through each one item in `packages.json`, for each package the script will:
   1. Gather the current version in `setup.py`
   2. Checks the current version against pypi.org's API database.
   3. If found, it will skip to the next package.
   4. If it doesn't find the package version in pypi's database, it will build it and deploy it.

**In short, the only way to deploy a package is to change it's version number manually in `setup.py`  for that specific package.** If the changes were made in the master branch, the deployment will go into production, for the dev branch, a postfix will be added to the name of the package before it is deployed to pypi. 

For example, you have commited all your changes to the master branch and you are ready to build and deploy the `agoutil` library, all you would need to do is to change the version number in `agolutil/setup.py` (ie `version="0.0.6"` to `version="0.0.7"`, you would simply save, commit and push to master. The CI script will do the rest for you (or not deploy if the version is already built).

## Development

We currently have two branches: master and dev. The master branch is used in production, our dev is meant for development and testing. 

### Dev & Master Postfix

For the dev branch, the build script will attach a post fix `"-dev"` to the package name specified in `setup.py`. For example, in the dev branch for the package name `agolutil/setup.py` we see the package name is `name="atd-agol-util"` and the current version was `0.0.6`, if you were to change the version number and commit to the dev branch, the deployment script will deploy to pypi as `atd-agol-util-dev`

### Pull Requests & Local Development

Pull requests are ignored by the CD/CI pipeline, meaning they do not get built. If you need a package built for dev testing:

- Test your script locally
- Create a PR against the dev branch, make sure you change the version number in setup.py
- Merge your PR branch to the dev branch

How about local development?

At the moment, local development is open-ended. You may use any python mechanism or style when including source python packages in your development and local tests.




#!/usr/bin/env bash

if [[ "${CIRCLE_BRANCH}" = "master" ]]; then
    export BUILD_ENV="master";
else
    export BUILD_ENV="dev";
fi;


#
# A helper function that prints a message in the build logs that is easy to identify.
#
function print_header {
    echo "----------------------------------------------------";
    echo ">> $1";
    echo "----------------------------------------------------";
    echo "";
}

#
# Prints a line for logging
#
function print_log {
    ENABLE_LOGGING="true"
    if [[ "${ENABLE_LOGGING}" = "true" ]]; then
        echo -e "$1";
    fi;
}

#
# Helps us determine the package version
# ie. build_get_package_version agolutil
#

function build_get_package_version {
    PACKAGE=$1;
    echo $(grep version setup.py | cut -d'"' -f 2);
}


#
# Returns true if the build already exists
#

function build_already_exists {
    PACKAGE=$1;
    PACKAGE_VERSION=$(build_get_package_version $PACKAGE);
    FOUND="false";

    # We need to change the postfix when in the dev environment.
    if [[ "${BUILD_ENV}" == "dev" ]]; then
        PACKAGE="${PACKAGE}-dev";
    fi;

    # We then check with pypi using their API to retrieve all published versions
    # jq will parse the api output, dev>null will take care of output errors to
    # prevent circleci from stopping the build.
    for VERSION_ITEM in $(curl --silent https://pypi.org/pypi/$PACKAGE/json | jq -r ".releases | keys[]" 2> /dev/null);
    do
        if [[ "${VERSION_ITEM}" = "${PACKAGE_VERSION}" ]]; then
            FOUND="true"
        fi;
    done;

    echo "${FOUND}";
}


#
# Returns the name of the environment
#

function build_resolve_environment {
    if [[ "${BUILD_ENVIRONMENT}" = "" ]]; then
        echo "dev";
    else
        echo "${BUILD_ENVIRONMENT}";
    fi;
}

#
# Patches the setup.py file in order to deploy a specific package environment
#
function build_patch_package_name {
    PACKAGE=$1
    POSTFIX=""
    print_header "build_patch_package_name() Patching package: ${PACKAGE}";

    # Only add postfix if not on master
    if [[ "${BUILD_ENV}" != "master" ]]; then
        POSTFIX="-${BUILD_ENV}";
    fi;

    sed -i "7s/${PACKAGE}/${PACKAGE}${POSTFIX}/" setup.py
}





#
# Build & Publish a single package.
# It assumes 'setup.py' is in the current working directory.
#
function build_single_package {
    PACKAGE=$1;
    print_header "build_single_package() building package: ${PACKAGE}";
    python3 setup.py sdist bdist_wheel;
}


#
# Deploys a built package into pypi.
# It assumes the 'dist' folder is in the current working directory.
#
function build_deploy_single_package {
    PACKAGE=$1;
    print_header "build_deploy_single_package() deploying package: ${PACKAGE}";
    print_log "build_deploy_single_package() twine upload --repository-url https://upload.pypi.org/legacy/ dist/*;"
    twine upload --repository-url https://upload.pypi.org/legacy/ dist/*;
}



#
# This function will return a list of all packages that need
# to be redeployed.
#

function build_packages {
    print_header "Building branch: ${BUILD_ENV}"

    for ATD_PACKAGE in $(jq -r ".packages[]" .circleci/packages.json);
    do
        #
        # Proceed only if the package can be found
        #
        if [ -e $ATD_PACKAGE/setup.py ];
        then
            print_log "build_packages() Package Found: ${ATD_PACKAGE}/setup.py";

            # First we need to switch to the package folder...
            cd $ATD_PACKAGE;

            # Gather package version and check if it already exists...
            PACKAGE_VERSION=$(build_get_package_version $ATD_PACKAGE);
            PACKAGE_EXISTS=$(build_already_exists $ATD_PACKAGE);

            # Skip build process if the current version is already built
            if [[ "${PACKAGE_EXISTS}" = "false" ]]; then
                build_patch_package_name $ATD_PACKAGE;
                build_single_package $ATD_PACKAGE;
                build_deploy_single_package $ATD_PACKAGE;
            else
                print_log "build_packages() The package '${ATD_PACKAGE}' is already deployed, skipping build process.";
                # We do not stop here because we may need to check other packages too..
            fi;

            cd ..;
        else
            print_log "build_packages() Could not find package ${ATD_PACKAGE}/setup.py";
        fi;
    done;

    print_header "build_packages() Finished build loop.";
}


#
# Returns a list of all the files changed in the current commit
#

function git_list_files_changed {
    git diff --name-only HEAD HEAD~1;
}
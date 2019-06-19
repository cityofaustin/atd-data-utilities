#!/usr/bin/env bash

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
# Helps us determine the package version
# ie. pypi_get_current_version agolutil
#

function pypi_get_current_version {
    PACKAGE=$1;
    VERSION=$(grep version $PACKAGE/setup.py | cut -d'"' -f 2);
    echo $VERSION;
}

#
# Increases the version of a specific package
#

function pypi_increase_version {
    PACKAGE=$1;
    CURRENT_VERSION=$(pypi_get_current_version $PACKAGE);

    print_header "Building package $PACKAGE";

    echo "bumpversion --current-version $CURRENT_VERSION minor setup.py"

    cd $PACKAGE;
    bumpversion --current-version $CURRENT_VERSION minor $PACKAGE/setup.py;
}




#
# Patches the setup.py file in order to deploy a specific package environment
#

function build_patch_branch_name {
    echo "Not yet implemented."
}


#
# Build & Publish a single package
#
function build_single_package {
    PACKAGE=$1;
    cd $PACKAGE;

    # Let's build our package distributables

    python3 setup.py sdist bdist_wheel;

    cd ..;
}

#
# This function will return a list of all packages that need
# to be redeployed.
#

function build_packages {
    export BUILD_ENV=$1

    print_header "Building branch: ${CIRCLE_BRANCH}"

    for ATD_PACKAGE in $(jq -r ".packages[]" .circleci/packages.json);
    do

        # pypi_increase_version $ATD_PACKAGE;

        build_single_package $ATD_PACKAGE;
    done;
}


#
# Returns a list of all the files changed in the current commit
#

function git_list_files_changed {
    git diff --name-only HEAD HEAD~1;
}
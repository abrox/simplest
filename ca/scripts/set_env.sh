#!/usr/bin/env bash
#Figure out directory where this script is located and set needed environment variables.
#koverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#There is most propably better way to dig out correct directories
#but... this is how it's now implementeded, sorry :-)
pushd $DIR > /dev/null 2>&1
pushd .. > /dev/null 2>&1
export CA_BASEDIR=$(pwd)
pushd ../server > /dev/null 2>&1
export EST_BASEDIR=$(pwd)
echo "CA_BASEDIR is $CA_BASEDIR and EST_BASEDIR: $EST_BASEDIR"
popd > /dev/null 2>&1
popd > /dev/null 2>&1
popd > /dev/null 2>&1

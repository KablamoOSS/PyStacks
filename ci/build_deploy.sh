#! /bin/bash

if [[ -z "$PYPI_USERNAME" || -z "$PYPI_PASSWORD" || -z "$PYPI_URL" ]]; then
    echo "You must set PYPI_USERNAME, PYPI_PASSWORD, and PYPI_URL to run this script"
    exit 1
fi
echo "Required environment variables are set ..."

SHORT_HASH=$(git rev-parse --short HEAD)
BUILD_VERSION=$(cat version.txt).${BITBUCKET_BUILD_NUMBER}
echo $BUILD_VERSION > version.txt
BUILD_VERSION=${BUILD_VERSION}-${SHORT_HASH}
echo "Building with version number: $BUILD_VERSION"

echo "Setting up pypi connection info ..."
cat << EOF > /root/.pypirc
[distutils]
index-servers=pypi

[pypi]
repository=${PYPI_URL}
username=${PYPI_USERNAME}
password=${PYPI_PASSWORD}
EOF

echo "Building pip package ..."
python setup.py sdist bdist_wheel           # Building package
echo "Uploading to pypi ($PYPI_URL) ..."
twine upload dist/*                         # Uploading to pypi

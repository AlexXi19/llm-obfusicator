#!/bin/bash
# Script to build and publish the package to PyPI

# Clean up previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
echo "Building the package..."
python setup.py sdist bdist_wheel

# Check the package
echo "Checking the package with twine..."
twine check dist/*

# Publish to TestPyPI first (optional)
read -p "Do you want to publish to TestPyPI? (y/n) " publish_test
if [ "$publish_test" = "y" ]; then
    echo "Publishing to TestPyPI..."
    twine upload --repository testpypi dist/*
    echo "Package published to TestPyPI!"
    echo "You can install it with: pip install --index-url https://test.pypi.org/simple/ llm-obfuscator"
fi

# Publish to PyPI
read -p "Do you want to publish to PyPI? (y/n) " publish_prod
if [ "$publish_prod" = "y" ]; then
    echo "Publishing to PyPI..."
    twine upload dist/*
    echo "Package published to PyPI!"
    echo "You can install it with: pip install llm-obfuscator"
fi 
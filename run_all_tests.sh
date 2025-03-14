#!/bin/bash

# Set the directory to the script's location
cd "$(dirname "$0")"

echo "===== Running Unit Tests ====="
python -m unittest discover tests

echo -e "\n===== Running Test Mapping Properties ====="
python tests/test_mapping_properties.py

echo -e "\n===== Running Test Obfuscation ====="
python tests/test_obfuscation.py

echo -e "\n===== Running Test Real World ====="
python tests/test_real_world.py

echo -e "\n===== All Tests Completed =====" 
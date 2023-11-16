#!/bin/bash

echo "Running Flake8..."
flake8 --config=./config/flake8_config.ini memory_test.py profile_deco.py

echo "Running Pylint..."
pylint --rcfile=./config/config_pylint.pylintrc memory_test.py profile_deco.py

echo "Lint checks completed."
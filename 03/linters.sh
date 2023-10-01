#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini custom_list.py

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc custom_list.py

echo "Lint checks completed."
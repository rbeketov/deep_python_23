#!/bin/bash

echo "Running Flake8..."
flake8 --config=./config/flake8_config.ini setup.py test_cjson.py

echo "Running Pylint..."
pylint --rcfile=./config/config_pylint.pylintrc setup.py test_cjson.py

echo "Lint checks completed."
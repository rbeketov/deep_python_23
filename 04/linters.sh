#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc

echo "Lint checks completed."
#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini tests src

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc tests
pylint --rcfile=config_pylint.pylintrc src

echo "Lint checks completed."
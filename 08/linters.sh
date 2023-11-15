#!/bin/bash

echo "Running Flake8..."
flake8 --config=./config/flake8_config.ini async_fetching.py test_async_fetching.py

echo "Running Pylint..."
pylint --rcfile=./config/config_pylint.pylintrc async_fetching.py test_async_fetching.py

echo "Lint checks completed."
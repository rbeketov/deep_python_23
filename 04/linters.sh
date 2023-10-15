#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini custom_meta.py test_custom_meta.py test_descriptor.py descriptor.py

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc custom_meta.py test_custom_meta.py test_descriptor.py descriptor.py

echo "Lint checks completed."
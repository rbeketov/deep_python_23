#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini json_generator.py mean_k_calls.py parse_json.py test_mean_k_calls.py test_parse_json.py

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc json_generator.py mean_k_calls.py parse_json.py test_mean_k_calls.py test_parse_json.py

echo "Lint checks completed."
#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini lru_cache.py test_lru_cache.py

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc lru_cache.py test_lru_cache.py

echo "Lint checks completed."
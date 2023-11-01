#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini client.py server.py test_client.py test_server.py

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc client.py server.py test_client.py test_server.py

echo "Lint checks completed."
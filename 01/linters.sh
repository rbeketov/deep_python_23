#!/bin/bash

echo "Running Flake8..."
flake8 --config=flake8_config.ini main.py model.py predict_mood.py rf_gen.py test_predict_mood.py test_rf_gen.py

echo "Running Pylint..."
pylint --rcfile=config_pylint.pylintrc main.py model.py predict_mood.py rf_gen.py test_predict_mood.py test_rf_gen.py

echo "Lint checks completed."
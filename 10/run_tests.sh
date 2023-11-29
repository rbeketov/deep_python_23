#!/bin/bash
echo "Running test..."
python3 -m unittest test_cjson.py
echo "Running test efficiency..."
python3 test_efficiency.py
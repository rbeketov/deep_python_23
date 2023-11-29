VENV := venv

.PHONY: all test clean

all: venv install setup linters

venv:
	python3 -m venv $(VENV) && \
	. $(VENV)/bin/activate && \
	pip install --upgrade pip

install: venv
	. $(VENV)/bin/activate && \
	pip install -r requirements.txt

setup: venv
	. $(VENV)/bin/activate && \
	python3 setup.py install

linters: venv
	. $(VENV)/bin/activate && \
	sh linters.sh

test: venv
	. $(VENV)/bin/activate && \
	sh run_tests.sh

clean:
	rm -rf $(VENV)

.DEFAULT_GOAL := all

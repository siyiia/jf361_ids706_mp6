install:
	pip install -r requirements.txt
lint:
	pylint --disable=R,C  --ignore-patterns=test_.*?py *.py
format:
	black *.py
test:
	python -m pytest -vv test_main.py
run:
	python main.py


all: install lint format test

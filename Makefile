install:
	pip install -r requirements.txt
lint:
	pylint --disable=R,C  --ignore-patterns=test_.*?py *.py
format:
	black *.py
run:
	python main.py


all: install lint format run

elp:
	echo "Cammands:1. build:  Builds the project 2. verify: Runs all test";

build:
	uv build

verify:
	uv run pytest --cov -s test_tt.py

cov:
	uv run pytest --cov --cov-report=html

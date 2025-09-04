help:
	echo "Cammands:1. build:  Builds the project 2. verify: Runs all test";

build:
	uv build

verify:
	uv run pytest


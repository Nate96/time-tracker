.PHONY: install

help:
	@echo "====Cammands===="
	@echo "1. install:  Adds alias to .zshrc"
	@echo "2. build:    Builds the project"
	@echo "3. verify:   Runs all test"
	@echo "4. coverage: Builds .htmlcov/"

install:
	@echo "alias tt='uv run --project $(realpath .) $(realpath tt.py)'" >> ~/.zshrc
	@echo "source ~/.zshrc"
	git branch local
	git checkout local

build:
	uv build

verify:
	uv run pytest --cov -s test_tt.py

cov:
	uv run pytest --cov --cov-report=html

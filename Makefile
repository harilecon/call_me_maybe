PYTHON = uv run python
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
FILE = src/*\
	   main.py


run: install
	$(PYTHON) main.py


install:
	uv sync


debug:
	$(PYTHON) -m pdb main.py


clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} \;
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete


lint:
	$(PYTHON) -m flake8 $(FILE)
	$(PYTHON) -m mypy $(FILE) $(MYPY_FLAGS)


lint-strict:
	$(PYTHON) -m flake8 $(FILE)
	$(PYTHON) -m mypy $(FILE) --strict

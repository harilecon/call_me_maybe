PYTHON = uv run uv run --python 3.12.5 python
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
FILE = src


run: install
	$(PYTHON) -m src


install:
	uv sync --python 3.12.5


debug:
	$(PYTHON) -m pdb src

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
	$(PYTHON) -m mypy $(FILE) --strict $(MYPY_FLAGS)

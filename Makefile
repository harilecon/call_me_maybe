PYTHON = uv run python
FILE = src/*\
	   main.py


run: install
	$(PYTHON)


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

PYTHON      = python3
MAP         = maps/easy/01_linear_path.txt
SRC         = main.py

install:
	$(PYTHON) -m pip install -r requirement.txt

run:
	$(PYTHON) $(SRC) $(MAP)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*_cache" -exec rm -rf {} +
	@echo "Clean complete"

lint:
	$(PYTHON) -m flake8 src $(SRC)
	$(PYTHON) -m mypy src $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 src $(SRC)
	$(PYTHON) -m mypy src $(SRC) --strict

debug:
	$(PYTHON) -m pdb $(SRC) $(MAP)

.PHONY: run clean lint lint-strict
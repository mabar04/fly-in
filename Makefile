PYTHON = python3
NAME = "maps/easy/01_linear_path.txt"

run:
	$(PYTHON) main.py $(NAME)

lint:
	flake8 . 
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs



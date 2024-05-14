.PHONY: install
install: ## Install Python requirements
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root

.PHONY: run
run: ## Run the project
	poetry run python -m src.app

.PHONY: format
format: ## Run formatter.
	poetry run python -m black .
	poetry run python -m isort .

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release/chores)
	poetry version patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release)
	poetry version minor

.PHONY: clean
clean: ## Clean project's temporary files (linux compatible)
	find . -wholename '*/.ipynb_checkpoints' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

VENV_NAME := .venv
VENV_ACTIVATE := $(VENV_NAME)/Scripts/activate

.PHONY: install
install: venv ## Install Python requirements
	$(VENV_NAME)/Scripts/python -m pip install --upgrade pip setuptools wheel poetry
	$(VENV_NAME)/Scripts/poetry lock
	$(VENV_NAME)/Scripts/poetry install --no-root
	$(VENV_NAME)/Scripts/poetry run pre-commit install

.PHONY: run
run: venv ## Run the project
	$(VENV_NAME)/Scripts/poetry run python -m src.app

.PHONY: notebook
notebook: venv ## Start Jupyter Notebook
	$(VENV_NAME)/Scripts/poetry run jupyter notebook --notebook-dir=src/notebooks/ --browser='open %s'

.PHONY: pre-commit
pre-commit: venv ## Run pre-commit checks
	$(VENV_NAME)/Scripts/poetry run pre-commit run --config ./.pre-commit-config.yaml

.PHONY: patch
patch: venv ## Bump project version to next patch (bugfix release/chores)
	$(VENV_NAME)/Scripts/poetry version patch

.PHONY: minor
minor: venv ## Bump project version to next minor (feature release)
	$(VENV_NAME)/Scripts/poetry version minor

.PHONY: clean-notebooks
clean-notebooks: venv ## Clean Jupyter Notebooks of output data
	$(VENV_NAME)/Scripts/find . -name '*.ipynb' | xargs -P 6 -n 1 $(VENV_NAME)/Scripts/poetry run python -m jupyter nbconvert --clear-output --inplace

.PHONY: clean
clean: venv ## Clean project's temporary files
	$(VENV_NAME)/Scripts/find . -wholename '*/.ipynb_checkpoints' -exec rm -rf {} +
	$(VENV_NAME)/Scripts/find . -name '__pycache__' -exec rm -rf {} +
	$(VENV_NAME)/Scripts/find . -name '*.pyc' -exec rm -f {} +
	$(VENV_NAME)/Scripts/find . -name '*.log' -exec rm -f {} +

.PHONY: venv
venv: $(VENV_ACTIVATE) ## Create virtual environment
$(VENV_ACTIVATE):
	python -m venv $(VENV_NAME)

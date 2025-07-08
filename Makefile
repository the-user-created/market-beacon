PACKAGE_NAME := market-beacon
VENV_NAME := ".$(PACKAGE_NAME)-venv"
VERSION_NUMBER := `cat CODE_VERSION.cfg`

.PHONY: help
help: ## This help dialog.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | \
	awk 'BEGIN {FS = "#"} {printf "%-30s %s\n", $$1, $$3}' | sed "s/\$$(PACKAGE_NAME)/$(PACKAGE_NAME)/g"

venv: ## Creates development environment and updates PIP - does NOT install requirements.
	python3.12 -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	python -m pip install --upgrade pip setuptools wheel build

.PHONY: lint
lint: ## Executes isort, black and flake8 on $(PACKAGE_NAME).
	. ${VENV_NAME}/bin/activate && \
	isort . && \
	black . && \
	flake8 .

.PHONY: install-deploy
install-deploy: ## Installs $(PACKAGE_NAME) without any devtools, for deployment.
	. ${VENV_NAME}/bin/activate && \
	python -m pip install .

.PHONY: install-dev
install-dev: ## Installs with all devtools, for development.
	. ${VENV_NAME}/bin/activate && \
	python -m pip install -e .[dev] && \
	pre-commit install && \
	pre-commit autoupdate

.PHONY: tests
execute-tests: ## Runs all unit tests.
	. ${VENV_NAME}/bin/activate && \
	python -m unittest discover tests/

.PHONY: increment-major-version
increment-major-version: ## Increments the major version number of $(PACKAGE_NAME).
	. ${VENV_NAME}/bin/activate && \
	bump2version --current-version ${VERSION_NUMBER} major CODE_VERSION.cfg
	git add .
	git commit -m "Incremented MAJOR version number."

.PHONY: increment-minor-version
increment-minor-version: ## Increments the minor version number of $(PACKAGE_NAME).
	. ${VENV_NAME}/bin/activate && \
	bump2version --current-version ${VERSION_NUMBER} minor CODE_VERSION.cfg
	git add .
	git commit -m "Incremented MINOR version number."

.PHONY: increment-patch-version
increment-patch-version: ## Increments the patch version number of $(PACKAGE_NAME).
	. ${VENV_NAME}/bin/activate && \
	bump2version --current-version ${VERSION_NUMBER} patch CODE_VERSION.cfg
	git add .
	git commit -m "Incremented PATCH version number."

.PHONY: run
run: ## Runs $(PACKAGE_NAME) with the given arguments.
	. ${VENV_NAME}/bin/activate && \
	exec python run.py $(args)

.PHONY: clean
clean: ## Removes the virtual environment and any compiled Python files.
	rm -rf ${VENV_NAME}
	rm -rf ${PACKAGE_NAME}.egg-info
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
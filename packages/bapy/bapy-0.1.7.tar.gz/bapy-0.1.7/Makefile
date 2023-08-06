.DEFAULT_GOAL := help

BUMP := patch  # major|minor|path
IMAGE := bapy
VERSION := latest

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
SHELL := $(shell command -v bash)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
CURRENT := $(shell git describe --abbrev=0 --tags 2>/dev/null; true)
DIR := $(shell dirname "$(realpath $(firstword $(MAKEFILE_LIST)))")
PROJECT := $(shell basename $(DIR))

ACTIVATE := $(DIR)/venv/bin/activate

######################################################## HELP ########################################################
.PHONY: help
help: ## print Makefile help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

######################################################## VARS ########################################################
.PHONY: vars
vars:  ## print Makefile vars
	@echo "BUMP: $(BUMP)"
	@echo "BRANCH: $(BRANCH)"
	@echo "CURRENT: $(CURRENT)"
	@echo "DIR: $(DIR)"
	@echo "PROJECT: $(PROJECT)"

######################################################## CLEAN ########################################################
.PHONY: clean
clean: clean-build clean-pyc clean-test clean-docker ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build:  ## remove build artifacts
	@/bin/rm -fr build/ > /dev/null 2>&1 | true
	@/bin/rm -fr dist/ > /dev/null 2>&1 | true
	@/bin/rm -fr .eggs/ > /dev/null 2>&1 | true
	@find . -name '*.egg-info' -exec /bin/rm -fr {} + > /dev/null 2>&1 | true
	@find . -name '*.egg' -exec /bin/rm -f {} + > /dev/null 2>&1 | true

.PHONY: clean-pyc
clean-pyc:  ## remove Python file artifacts
	@find . -name '*.pyc' -exec /bin/rm -f {} + > /dev/null 2>&1 | true
	@find . -name '*.pyo' -exec /bin/rm -f {} + > /dev/null 2>&1 | true
	@find . -name '*~' -exec /bin/rm -f {} + > /dev/null 2>&1 | true
	@find . -name '__pycache__' -exec /bin/rm -fr {} + > /dev/null 2>&1 | true

.PHONY: clean-test
clean-test:  ## remove test and coverage artifacts
	@/bin/rm -fr .tox/ > /dev/null 2>&1 | true
	@/bin/rm -fr .pytest_cache > /dev/null 2>&1 | true
	@find . -name '.mypy_cache' -exec /bin/rm -rf {} + > /dev/null 2>&1 | true

.PHONY: clean-docker
clean-docker:  ## Example: make clean_docker VERSION=latest, make clean_docker IMAGE=some_name VERSION=0.1.0
	@docker rmi -f $(IMAGE):$(VERSION) > /dev/null 2>&1 | true

######################################################## TEST ########################################################
.PHONY: test
test: clean darglint doctest pytest  ## all tests

.PHONY: darglint
darglint: clean  ## darglint docstrings tests
	@source "$(ACTIVATE)" && darglint -v 2 -s google --log-level DEBUG --strictness full $(PROJECT)/*.py

.PHONY: mypy
mypy: clean  ## mypy tests - does not work
	@true || cd $(PROJECT) && source "$(ACTIVATE)" && mypy --config-file $(DIR)/setup.cfg --show-traceback *.py

.PHONY: doctest
doctest: clean  ## doctest tests
	@source "$(ACTIVATE)" && python -m doctest $(PROJECT)/*.py  # -v

.PHONY: pytest
pytest: clean  ## pytest tests
	@source "$(ACTIVATE)" && pytest

######################################################## DOCKER ########################################################
.PHONY: docker
docker: clean  ## Example: make docker VERSION=latest, make docker IMAGE=some_name VERSION=0.1.0
	@echo Building docker $(IMAGE):$(VERSION)
	@docker build -t $(IMAGE):$(VERSION) . -f ./docker/Dockerfile --no-cache

######################################################### GIT ########################################################
.PHONY: git
git: add bump push  # git add, bump version and git push

.PHONY: add
add:  ## git add all
	@git add . --all

.PHONY: bump
bump:  ## bump2version
	@bump2version --allow-dirty $(BUMP)

.PHONY: push
push:  ## git push
	@git push -u origin $(BRANCH) --tags

######################################################## DIST ########################################################
.PHONY: dist
dist: test git build upload install merge clean## builds source and wheel package

.PHONY: build
build:  ## build sdist and wheel
	@source "$(ACTIVATE)" && python setup.py sdist
	@source "$(ACTIVATE)" && python setup.py bdist_wheel
	@ls -l dist

.PHONY: upload
upload:  ## build sdist nd wheel
	@source "$(ACTIVATE)" && twine upload -r jose-nferx dist/*

.PHONY: install
install:  ## installs in system
	$$( which python3.8 ) -m pip install -vvvv --upgrade $(PROJECT)

.PHONY: merge
merge:  ## installs in system
ifneq ($(BRANCH),master)
	@echo "BRANCH: $(BRANCH)"
	@git checkout master
	@git merge $(BRANCH)
	@echo "BRANCH: $$(git rev-parse --abbrev-ref HEAD)"
	@gall
	@echo "To delete locally: git branch -d $(BRANCH)"
	@echo "To delete locally: git push origin --delete  $(BRANCH)"
else
	@echo "BRANCH: $(BRANCH) - Nothing to do here."
endif

PYTHON_DIST_NAME := warp-dev-backup
BINARY_FILES := bin/wdb

COMMIT_ISH := $(shell git rev-parse --quiet --verify --short HEAD || echo "None")
BUILD_DATE := $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
PYTHON_VERSION := $(shell python3 --version)
CONTAINER_ENV ?= false

PYTHON_BIN ?= venv/bin/python3
PIP_BIN ?= venv/bin/pip3

ifeq ($(CONTAINER_ENV),true)
PYTHON_BIN := /usr/local/bin/python3
PIP_BIN := /usr/local/bin/pip3
endif

PYTEST_CONFIG_FILE := pytest.ini
ifdef DEBUG
PYTEST_CONFIG_FILE := pytest.debug.ini
endif


.PHONY: init
init: bootstrap

.PHONY: bootstap
bootstrap: venv install

.PHONY: pythonversion
pythonversion:
	@echo "using ${PYTHON_VERSION}"

.PHONY: venv
venv: pythonversion clean
	rm -rf venv || true
	python3 -m venv venv
	$(PIP_BIN) install --upgrade pip build #setuptools wheel

.PHONY: install
install:
	$(PIP_BIN) install -e .[dev]

.PHONY: uninstall
uninstall:
	$(PIP_BIN) uninstall -y --no-input $(PYTHON_DIST_NAME)
	rm $(BINARY_FILES) || true
	rm -rf src/*.egg-info


.PHONY: test
test:
	$(PYTHON_BIN) -m pytest -c $(PYTEST_CONFIG_FILE) tests/

.PHONY: cover
cover:
	$(PYTHON_BIN) -m pytest -c $(PYTEST_CONFIG_FILE) --cov=src tests/

.PHONY: cover-html
cover-html:
	$(PYTHON_BIN) -m pytest -c $(PYTEST_CONFIG_FILE) --cov=src --cov-report=html tests/

.PHONY: clean
clean:
	rm -rf build dist src/*.egg-info

.PHONY: clean-test
clean-test:
	rm -rf reports/

.PHONY: clean-tmp
clean-tmp:
	rm -rf .pytest_cache **/.pytest_cache


build:
	$(PYTHON_BIN) -m build

.PHONY: upload
upload:
	# Specify repository from ~/.pypirc by defining -r ${TARGET_REPO}
	$(PYTHON_BIN) -m twine upload dist/*

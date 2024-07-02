# Makefile for automating build, run, and test commands on both Windows and Linux

# Variables
SYS_PYTHON=python3
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip
ACTIVATE=$(VENV_DIR)/bin/activate
POETRY=$(VENV_DIR)/bin/poetry
RMRF=rm -rf

# Determine the platform and set variables accordingly (for those poorest of souls that try to develop on Windows)
ifeq ($(OS),Windows_NT)
	SYS_PYTHON=python
    PYTHON=.\$(VENV_DIR)\Scripts\python.exe
    PIP=.\$(VENV_DIR)\Scripts\pip.exe
    ACTIVATE=.\$(VENV_DIR)\Scripts\activate
    POETRY=.\$(VENV_DIR)\Scripts\poetry
    RMRF=rd /s /q #this one... after all the years they refuse to accept GNU syntax
endif

# Target to create virtual environment and install dependencies using Poetry
$(ACTIVATE): pyproject.toml check-python
	@echo "Creating virtual environment..."
	$(SYS_PYTHON) -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install poetry
	$(POETRY) install

# Check for system Python and pip
.PHONY: check-python
check-python:
	@echo "Checking for system Python..."
	@which $(SYS_PYTHON) > /dev/null || (echo "Error: $(SYS_PYTHON) is not installed."; exit 1)
	@echo "System Python is installed."

# Build: Set up the environment and install dependencies
.PHONY: build
build: $(ACTIVATE)
	@echo "Environment setup complete."

# Run: Start the application
.PHONY: run
run: build
	@echo "Starting the application..."
	fastapi run

# dev: Run the dev mode with reloads
.PHONY: dev
dev: build
	@echo "Starting the application dev mode..."
	$(POETRY) run dotenv -f .env run fastapi dev --reload

# Test: Run the test suite
.PHONY: test
test: build
	@echo "Running tests..."
	$(POETRY) run dotenv -f .env.test run pytest

# Clean: Remove the virtual environment
.PHONY: clean
clean:
	@echo "Cleaning up..."
	$(RMRF) $(VENV_DIR)

# Help: Show available targets
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build         Set up the environment and install dependencies"
	@echo "  run           Start the application"
	@echo "  test          Run the test suite"
	@echo "  dev           Run the dev mode with reloads"
	@echo "  clean         Remove the virtual environment"
	@echo "  check-python  Check the system python installation"
	@echo "  help          Show this help message"

# Project Chimera: The Governor Command Center
.PHONY: setup test run clean lint spec-check help

# Variables
PYTHON = python3
PIP = pip
PYTEST = pytest
ENV = CHIMERA_ENV=testing

# Default command
help:
	@echo "Project Chimera Build System"
	@echo "---------------------------"
	@echo "setup      : Install dependencies and link local packages"
	@echo "test       : Run the TDD test suite (Standard & Performance)"
	@echo "lint       : Run security (Bandit) and style (Flake8/Black) checks"
	@echo "spec-check : Verify alignment with technical and functional specs"
	@echo "run        : Boot the main Agent/API"
	@echo "clean      : Purge caches and temporary build files"

# 1. Setup Phase
setup:
	@echo "🔧 Installing requirements..."
	$(PIP) install -r requirements.txt
	@echo "🔗 Linking Skill Packages..."
	$(PIP) install -e .
	@echo "✅ Setup Complete. Check MCP Connection manually if required."

# 2. Quality & Security (Task 3.2)
lint:
	@echo "🛡️  Running Security Audit (Bandit)..."
	bandit -r skills/
	@echo "🎨 Running Style Check (Flake8)..."
	flake8 skills/ --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "🧹 Formatting Code (Black)..."
	black .

# 3. Testing Phase (Task 3.1)
test:
	@echo "🚀 Running TDD Failing Tests..."
	$(ENV) $(PYTEST) tests/ -v

# 4. Governance Phase
spec-check:
	@echo "🔍 Verifying Spec Alignment..."
	@ls specs/functional.md specs/technical.md > /dev/null || (echo "❌ ERROR: Missing spec files!"; exit 1)
	@echo "✅ Specifications present in /specs directory."

# 5. Execution
run:
	@echo "🤖 Starting Project Chimera..."
	$(PYTHON) main.py

# 6. Cleanup
clean:
	@echo "🧼 Cleaning workspace..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf .venv
	@echo "✨ Workspace cleared."
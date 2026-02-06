.PHONY: setup test run clean

# Install dependencies
setup:
	pip install -r requirements.txt

# Run the test suite with the temporary SQLite database
test:
	CHIMERA_ENV=testing pytest tests/ -v

# Run the main application (requires Postgres)
run:
	python3 main.py

# Remove temporary python files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f .pytest_cache

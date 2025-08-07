.PHONY: install install-pip poetry-export-requirements validate-graph-poetry validate-graph-pip help clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install                      - Install dependencies using Poetry"
	@echo "  install-pip                  - Install dependencies using pip from requirements.txt"
	@echo "  poetry-export-requirements   - Export requirements to requirements.txt"
	@echo "  validate-graph-poetry        - Run graph validation script using Poetry"
	@echo "  validate-graph-pip           - Run graph validation script using pip"
	@echo "  clean                        - Clean up temporary files"
	@echo "  help                         - Show this help message"

install:
	poetry install

install-pip:
	pip install -r requirements.txt

poetry-export-requirements:
	poetry run pip freeze > requirements.txt

# Run graph validation
validate-graph-poetry:
	poetry run python scripts/validate_entity_graph.py

validate-graph-pip:
	python3 scripts/validate_entity_graph.py

run-agent-poetry:
	poetry run python agent.py

run-agent-pip:
	python3 agent.py

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
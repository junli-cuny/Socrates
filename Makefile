# Makefile for the Socrates LLM Education Tool

.PHONY: help install create run serve grade report clean

# Default target: show help message.
help:
	@echo "Socrates LLM Education Tool Makefile"
	@echo "------------------------------------"
	@echo "Available commands:"
	@echo "  make install                - Installs required Python dependencies"
	@echo "  make create FILE=<path>     - Creates an assignment from a question JSON file"
	@echo "  make run                    - Launches the classic Jupyter Notebook server"
	@echo "  make serve NOTEBOOK=<path>  - Serves a specific notebook as a web app using Voila"
	@echo "  make grade ASSIGNMENT=<path> - Grades submissions and generates an HTML report"
	@echo "  make report                 - Generates an HTML report from the last grading run"
	@echo "  make clean                  - Removes all generated files and reports"

# Target to install dependencies
install:
	@echo "Installing dependencies..."
	pip3 install -r requirements.txt
	@echo "Installation complete."

# Target to create an assignment
create:
ifeq ($(FILE),)
	@echo "Error: Specify a file. Usage: make create FILE=<path/to/questions.json>"
	@exit 1
endif
	@echo "Creating assignment from $(FILE)..."
	python3 src/create_assignment.py $(FILE)

# Target to launch Jupyter Notebook
run:
	@echo "Starting Jupyter Notebook server..."
	jupyter notebook

# Target to serve a notebook with Voila
serve:
ifeq ($(NOTEBOOK),)
	@echo "Error: Specify a notebook. Usage: make serve NOTEBOOK=<path/to/notebook.ipynb>"
	@exit 1
endif
	@echo "Serving $(NOTEBOOK) with Voila..."
	voila $(NOTEBOOK) --no-browser --port=8866

# Target to grade all submissions AND generate a report
grade:
ifeq ($(ASSIGNMENT),)
	@echo "Error: Specify the master assignment file. Usage: make grade ASSIGNMENT=<path/to/questions.json>"
	@exit 1
endif
	@echo "Grading all submissions against $(ASSIGNMENT)..."
	python3 src/grade.py $(ASSIGNMENT)
	@$(MAKE) report

# Target to generate the HTML report
report:
	@echo "Generating HTML grading report..."
	python3 src/generate_report.py

# Target to clean up generated files
clean:
	@echo "Cleaning up generated files..."
	rm -f result/*.ipynb result/*.json
	rm -f src/grading_results.json
	rm -f grading_report.html
	find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Cleanup complete."

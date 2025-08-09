import json
import nbformat as nbf
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found. Please create a .env file.")

if len(sys.argv) < 2:
    print("Usage: python create_assignment.py <path_to_question_file.json>")
    sys.exit(1)

# Define base directories
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent
RESULTS_DIR = PROJECT_ROOT / "result"
RESULTS_DIR.mkdir(exist_ok=True)

# --- FUNCTIONS ---
def load_json_file(file_path):
    """Generic function to load and validate a JSON file."""
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON in {file_path}.")
        return None

# --- SCRIPT LOGIC ---
questions_filepath = Path(sys.argv[1])
# --- MODIFIED PATH ---
# The whitelist is now in the 'assignment' directory at the project root.
whitelist_filepath = PROJECT_ROOT / "assignment" / "whitelist.json"

questions_data = load_json_file(questions_filepath)
if not questions_data or "questions" not in questions_data:
    print("Error: Invalid question file format.")
    sys.exit(1)

whitelist_data = load_json_file(whitelist_filepath)
if not whitelist_data or "passcodes" not in whitelist_data:
    print(f"Warning: Could not load passcodes from {whitelist_filepath}. Verification will be disabled.")
    passcodes = []
else:
    passcodes = whitelist_data["passcodes"]

# --- The rest of the script remains the same ---
# Create a new notebook
notebook = nbf.v4.new_notebook()

# Cell 1: Initialize Playground
initialize_playground = [
    "import sys, os\n",
    "parent_directory = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))\n",
    "if parent_directory not in sys.path:\n",
    "    sys.path.append(parent_directory)\n",
    "from playground import Playground\n",
    "p = Playground()\n"
]
notebook["cells"].append(nbf.v4.new_code_cell("".join(initialize_playground)))

# Cell 2: Set LLM Model
notebook["cells"].append(nbf.v4.new_code_cell("p.set_model('gpt-4o-mini')"))

# Cell 3: Student Verification (dynamically populated)
whitelist_lines = []
for passcode in passcodes:
    whitelist_lines.append(f"p.add_whitelist('{passcode}')\n")
whitelist_lines.append("p.create_verify()\n")
notebook["cells"].append(nbf.v4.new_code_cell("".join(whitelist_lines)))

# ... (rest of the question generation logic) ...
for question in questions_data["questions"]:
    markdown_cell = nbf.v4.new_markdown_cell(f"# Question {question['id']}: {question['text']}")
    notebook["cells"].append(markdown_cell)

    code_cell_lines = []
    if len(question.get("instructions", [])) == 1:
        instruction_escaped = question['instructions'][0].replace("'", "\\'")
        testcases = question.get("testcases", [])
        code_cell_lines.append(f"instruction = '{instruction_escaped}'")
        code_cell_lines.append(f"testcases = {testcases}")
        code_cell_lines.append("p.create_question()")
        code_cell_lines.append("p.add_instruction(instruction, testcases if testcases else None)")
    else:
        code_cell_lines.append("p.create_question()")
        for i, instruction in enumerate(question["instructions"]):
            instruction_escaped = instruction.replace("'", "\\'")
            code_cell_lines.append(f"p.add_instruction('{instruction_escaped}')")
        if "questionToGrade" in question and question["questionToGrade"]:
            final_instruction_escaped = question["questionToGrade"].replace("'", "\\'")
            code_cell_lines.append(f"p.add_instruction('Final Part: {final_instruction_escaped}')")

    code_cell_lines.append("p.displayAll()")
    notebook["cells"].append(nbf.v4.new_code_cell("\n".join(code_cell_lines)))

notebook["cells"].append(nbf.v4.new_code_cell("p.store_final_answer()"))

output_filename_base = questions_filepath.stem
output_filename = f"{output_filename_base}.ipynb"
output_filepath = RESULTS_DIR / output_filename

with open(output_filepath, "w") as file:
    nbf.write(notebook, file)

print(f"\nSuccess! Notebook saved as {output_filepath}")

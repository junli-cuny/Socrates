import sys
import json
from pathlib import Path
from Grader import Grader

def main():
    if len(sys.argv) < 2:
        print("Usage: python grade.py <path_to_assignment_file.json>")
        sys.exit(1)

    assignment_file = Path(sys.argv[1])
    if not assignment_file.is_file():
        print(f"Error: Assignment file not found at {assignment_file}")
        sys.exit(1)

    print("--- Starting Automated Grading Process ---")

    codes_dir = Path(__file__).parent
    results_dir = codes_dir.parent / "result"
    answer_files = list(results_dir.glob("answers_*.json"))

    if not answer_files:
        print(f"No student answer files found in '{results_dir}'.")
        return

    # Initialize the grader and load the master assignment
    g = Grader()
    g.load_assignment(assignment_file)

    # Load each student's answers
    for file_path in answer_files:
        student_id = file_path.name
        with open(file_path, 'r', encoding='utf-8') as f:
            g._student_answers[student_id] = json.load(f)

    # Run the grading process
    g.grade()
    print("--- Automated Grading Complete ---")

if __name__ == "__main__":
    main()

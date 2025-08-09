from LLM import *
import ipywidgets as widgets
from IPython.display import display
import json
import time

class Grader:
  def __init__(self):
    self._student_answers = {}
    self._model = "gpt-4o-mini"
    self.llm = LLM(model=self._model)
    self._master_questions = {} # To store the authoritative questions
    self.final_results = {}

  def set_model(self, model):
    self._model = model
    self.llm = LLM(model=self._model)

  def load_assignment(self, assignment_path):
    """Loads the master question file as the source of truth."""
    try:
        with open(assignment_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Index questions by their ID for easy lookup (e.g., 'q1', 'q2')
            for q in data.get('questions', []):
                q_id = f"q{q['id']}"
                self._master_questions[q_id] = q
        print(f"Successfully loaded assignment template from: {assignment_path}")
    except Exception as e:
        print(f"Error loading assignment file: {e}")

  def create_upload_button(self):
    upload_widget = widgets.FileUpload(accept='.json', description='Upload Answers', multiple=True)
    def handle_upload(change):
      self._student_answers.clear()
      for file_info in upload_widget.value:
        content = file_info['content'].tobytes()
        student_id = file_info["name"]
        self._student_answers[student_id] = json.loads(content.decode('utf-8'))
        print(f"Uploaded: {student_id}")
    upload_widget.observe(handle_upload, names='value')
    display(upload_widget)

  def grade(self):
    """Grades all uploaded student answers against the master assignment."""
    if not self._student_answers:
      print("No student answers uploaded.")
      return
    if not self._master_questions:
      print("No master assignment file loaded. Please load one first.")
      return

    for student_id, student_submission in self._student_answers.items():
      print(f"\n--- Grading student: {student_id} ---")
      result = {}
      for q_id, student_content in student_submission.items():
        if q_id not in self._master_questions:
            print(f"Warning: Question {q_id} from student submission not found in master assignment. Skipping.")
            continue

        print(f"--- Grading question: {q_id} ---")

        master_question = self._master_questions[q_id]
        student_answers = student_content['answers']

        # Use master instructions and testcases, NOT student-submitted ones
        instructions = master_question.get('instructions', [])
        testcases = master_question.get('testcases', [])

        if testcases: # It's a single-instruction question with test cases
            time, rates, avg, history = self.llm.grade_one_question(instructions, student_answers, testcases, stream=False)
        else: # It's a multi-part conceptual question
            time, rates, avg, history = self.llm.grade_multiple_question(instructions, student_answers, stream=False)

        result[q_id] = {'time': time, 'rates': rates, 'avg_rates': avg, 'test_history': history}
      self.final_results[student_id] = result

    print("\n--- Grading Complete ---")
    self.output_score()

  def output_score(self):
    output_filename = 'grading_results.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
      json.dump(self.final_results, f, indent=4)
    print(f"Grading results saved to {output_filename}")

  def run(self):
    button = widgets.Button(description='Start Grading', button_style='success')
    button.on_click(lambda x: self.grade())
    display(button)

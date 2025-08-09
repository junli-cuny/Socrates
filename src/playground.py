import ipywidgets as widgets
from IPython.display import display, clear_output
import json
from LLM import LLM  # Corrected import
import copy

class Playground:

    def __init__(self):
        # used to keep track of the current question
        self._curr_question = ''
        self._curr_index = 0
        # stores all the questions, instructions, answers, and testcases as WIDGET OBJECTS
        self._displayable = {}
        # verification system
        self._verified = False
        self._userID = None
        self._whitelist = []
        # used for LLM grading. The LLM class now handles the API key.
        self._model = "gpt-4o-mini"
        self.llm = LLM(model=self._model)

    def set_model(self, model):
        """Sets the model for the LLM and re-initializes it."""
        self._model = model
        self.llm = LLM(model=model)

    def add_whitelist(self, userID):
        """Temporary whitelist, should not be visible to student in a real scenario."""
        self._whitelist.append(userID)

    def verify(self, userID=''):
        """Used to verify if an acceptable userID was inputted."""
        self._verified = userID in self._whitelist
        self._userID = userID

    def __isVerified(self):
        return self._verified

    def create_verify(self):
        """Creates widgets for student ID verification."""
        id_input = self.create_textarea("Enter your student ID", height='40px')
        output = widgets.Output()

        def test_verify(id_value, out):
            with out:
                clear_output()
                self.verify(id_value)
                if self.__isVerified():
                    print("You are verified.")
                else:
                    print("You are not verified. Please enter a valid ID to test your answers.")

        display(
            id_input,
            self.create_button("Verify", on_click=lambda b: test_verify(id_input.value.strip(), output)),
            output
        )

    def create_textarea(self, placeholder='Enter your answer here', value='', width='80%', height='200px'):
        return widgets.Textarea(
            placeholder=placeholder,
            value=value,
            layout=widgets.Layout(width=width, height=height)
        )

    def create_button(self, description='Submit', on_click=None):
        button = widgets.Button(description=description)
        if on_click:
            button.on_click(on_click)
        return button

    def create_dropdown(self, options=[]):
        return widgets.Dropdown(options=options)

    def create_label(self, value=''):
        return widgets.Label(value=value)

    def create_question(self, question_text=None):
        self._curr_index += 1
        self._curr_question = f'q{self._curr_index}'
        self._displayable[self._curr_question] = {}
        if question_text:
            self._displayable[self._curr_question]['question'] = self.create_label(value=question_text)

    def add_instruction(self, instruction, testcases=None, initial_value=''):
        if 'instructions' not in self._displayable[self._curr_question]:
            self._displayable[self._curr_question]['instructions'] = []
            self._displayable[self._curr_question]['answers'] = []

        self._displayable[self._curr_question]['instructions'].append(self.create_label(value=instruction))
        self._displayable[self._curr_question]['answers'].append(self.create_textarea(value=initial_value))

        if testcases:
            if not isinstance(testcases, list):
                testcases = [testcases]
            self._displayable[self._curr_question]['testcases'] = self.create_dropdown(options=testcases)

    def displayAll(self):
        curr_question_widgets = self._displayable[self._curr_question]

        # Display instructions and answer text areas
        for i in range(len(curr_question_widgets['instructions'])):
            if len(curr_question_widgets['instructions']) > 1:
                display(curr_question_widgets['instructions'][i])
            display(curr_question_widgets['answers'][i])

        # Display test cases dropdown if it exists
        if 'testcases' in curr_question_widgets:
            display(curr_question_widgets['testcases'])

        # Output widget for feedback and the "Test" button
        output_widget = widgets.Output()
        q_id = copy.deepcopy(self._curr_question)
        button_widget = self.create_button("Test", on_click=lambda b: self.student_test_button(b, q_id, output_widget))

        display(button_widget, output_widget)

    def student_test_button(self, b, question_id, output):
        with output:
            clear_output()
            if not self.__isVerified():
                print("You are not authorized to test answers. Please verify your ID.")
                return

            content = self.convertToText(self._displayable[question_id])

            print("--- Grading your answer... ---")

            if 'testcases' in content and content['testcases']:
                # This is a single-instruction question with test cases
                time, rates, avg_rates, test_history = self.llm.grade_one_question(content['instructions'], content['answers'], content['testcases'], stream=True)
            else:
                # This is a multi-instruction conceptual question
                time, rates, avg_rates, test_history = self.llm.grade_multiple_question(content['instructions'], content['answers'], stream=True)

            if 'test_history' not in self._displayable[question_id]:
                self._displayable[question_id]['test_history'] = []

            dict_output = {
                'time': time,
                'rates': rates,
                'avg_rates': avg_rates,
                'test_history': test_history
            }
            self._displayable[question_id]['test_history'].append(dict_output)

    def convertToText(self, curr_question_widgets):
        dict_output = {}
        if 'question' in curr_question_widgets:
            dict_output['question'] = curr_question_widgets['question'].value

        dict_output['instructions'] = [instr.value for instr in curr_question_widgets['instructions']]
        dict_output['answers'] = [ans.value for ans in curr_question_widgets['answers']]

        if 'testcases' in curr_question_widgets:
            dict_output['testcases'] = [curr_question_widgets['testcases'].value]

        return dict_output

    def convertToJSON(self):
        json_output = {}
        for q_id, widgets_dict in self._displayable.items():
            json_output[q_id] = {}

            if 'question' in widgets_dict:
                json_output[q_id]['question'] = widgets_dict['question'].value

            json_output[q_id]['instructions'] = [instr.value for instr in widgets_dict['instructions']]
            json_output[q_id]['answers'] = [ans.value for ans in widgets_dict['answers']]

            if 'testcases' in widgets_dict:
                json_output[q_id]['testcases'] = [widgets_dict['testcases'].value]

            if 'test_history' in widgets_dict:
                json_output[q_id]['test_history'] = widgets_dict['test_history']
        return json_output

    def store_final_answer(self):
        """Creates a submit button that saves all answers to a local JSON file."""
        output_widget = widgets.Output()

        def format_and_write(out):
            with out:
                clear_output()
                if not self._userID:
                    print("Cannot submit without a user ID. Please verify first.")
                    return

                json_data = self.convertToJSON()
                # Save the file in the current directory (where the notebook is)
                filename = f"answers_{self._userID}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4)
                print(f"Submission successful! Answers saved to {filename}")

        button_widget = self.create_button("Submit Assignment", on_click=lambda b: format_and_write(output_widget))
        display(button_widget, output_widget)

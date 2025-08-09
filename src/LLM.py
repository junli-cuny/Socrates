from openai import OpenAI
import time
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class LLM:
  def __init__(self, model="gpt-4o-mini") -> None:
    self.api_key = os.getenv("OPENAI_API_KEY")
    if not self.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    self.model = model
    self.client = OpenAI(api_key=self.api_key)

  def chat_completion_openai(self, prompt, retries=3, stream=False, usageInfo=False):
        """Makes a call to the OpenAI API and handles retries."""
        last_exception = None
        for i in range(retries):
            try:
                t1 = time.time()
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7, # Slightly lower temp for more consistent grading
                    stream=stream
                )
                total_time = time.time() - t1

                if not stream:
                    content = response.choices[0].message.content.strip()
                    if usageInfo:
                        return content, dict(response.usage), [total_time]
                    return content
                else:
                    # Handle streaming response
                    complete_response = ""
                    for chunk in response:
                        if chunk.choices[0].delta.content is not None:
                            complete_response += chunk.choices[0].delta.content
                            print(chunk.choices[0].delta.content, end='', flush=True) # Stream to console
                    print("\n") # Newline after streaming is done
                    return complete_response.strip()

            except Exception as e:
                last_exception = e
                if "rate limit" in str(e).lower():
                    print(f"Rate limit hit. Retrying in {2**i} seconds...")
                    time.sleep(2**i)
                else:
                    print(f"An unexpected error occurred: {e}")
                    break # Don't retry on non-rate-limit errors

        raise ConnectionError(f"Failed to get response from OpenAI after {retries} retries.") from last_exception


  def compare(self, llm_answer, correct_answer_fragment):
    """Compares an LLM's generated answer with an expected fragment."""
    prompt = f"Does the following text: \"{llm_answer}\" correctly address the concept of \"{correct_answer_fragment}\"? Respond with only 'Yes' or 'No'."
    out = self.chat_completion_openai(prompt)
    verification_history = prompt + "\n" + out
    return "yes" in out.lower(), verification_history

  def grade_one_question(self, instructions, student_answer, testcases, threshold=0.5, stream=False):
    """Grades a single-instruction question against multiple test cases."""
    test_history = ""
    rates = []
    student_full_answer = f"The student's explanation is: '{student_answer[0]}'. "
    instruction_text = instructions[0]
    start_time = time.time()

    print(f"--- Evaluating Question: {instruction_text} ---")
    for i, testcase in enumerate(testcases):
        print(f"\n========== Test Case {i+1}: '{testcase}' ==========")
        prompt = f"""
        You are a teaching assistant evaluating a student's answer to a computer science question.

        Question instruction: "{instruction_text}"
        Student's answer: "{student_full_answer}"

        Your task is to determine if the student's answer correctly applies to the following test case: "{testcase}".

        Think step-by-step and provide a brief explanation of why the student's answer succeeds or fails for this specific test case. Conclude your entire response with a single word: "Correct" if it succeeds, or "Incorrect" if it fails.
        """
        test_history += f"Prompt for test case '{testcase}':\n{prompt}\n\n"

        success = 0
        attempts = 0
        for j in range(3): # Retry up to 3 times for consistency
            attempts += 1
            llm_evaluation = self.chat_completion_openai(prompt, stream=stream)
            test_history += f"Attempt {j+1} Evaluation:\n{llm_evaluation}\n\n"

            if "correct" in llm_evaluation.lower()[-20:]: # Check the end of the response
                print(f"--- Test Case {i+1} Passed ---")
                success += 1
                break
            else:
                if j == 2:
                    print(f"--- Test Case {i+1} Failed ---")

        rate = float(success) / attempts
        rates.append(rate)

    end_time = time.time()
    avg_rate = sum(rates) / len(rates) if rates else 0

    print(f"\n--- Final Result ---")
    if avg_rate >= threshold:
        print(f"Success Rate: {avg_rate:.2f}. Your answer is accepted.")
        test_history += "\nOverall Result: Accepted"
    else:
        print(f"Success Rate: {avg_rate:.2f}. Does not meet threshold of {threshold}. Please revise your answer.")
        test_history += f"\nOverall Result: Not Accepted (Threshold: {threshold})"

    return end_time - start_time, rates, avg_rate, test_history

  def grade_multiple_question(self, instructions, student_answers, stream=False):
    """Grades a conceptual, multi-part question without discrete test cases."""
    start_time = time.time()

    # Combine instructions and answers for a holistic review
    full_context = ""
    for i, instruction in enumerate(instructions):
        answer = student_answers[i] if i < len(student_answers) else "[No answer provided]"
        full_context += f"Instruction {i+1}: {instruction}\nStudent's Answer {i+1}: {answer}\n\n"

    prompt = f"""
    You are a helpful teaching assistant providing feedback on a multi-part computer science question.
    Below are the instructions the student was given and their corresponding answers.

    {full_context}

    Your task is to:
    1. Review all the student's answers in the context of the instructions.
    2. Provide constructive feedback on each part.
    3. Explain what they did well and where they can improve.
    4. Do NOT give the direct, correct answer. Guide the student toward it.

    Please provide your feedback now.
    """

    print("--- Evaluating your response... ---")
    feedback = self.chat_completion_openai(prompt, stream=stream)
    end_time = time.time()

    # For multi-part questions, the "rate" is qualitative. We return 1.0 for completion.
    # The 'test_history' is the qualitative feedback itself.
    return end_time - start_time, [1.0], 1.0, feedback

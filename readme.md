# Socrates: The LLM-Powered Learning Tool

## Description

Socrates is a learning tool that leverages Large Language Models (LLMs) to help students learn computer science concepts. Unlike traditional methods that provide direct answers, Socrates requires students to first attempt an answer. The LLM then provides constructive feedback, guiding them to discover the correct solution themselves. This Socratic method encourages critical thinking and deeper engagement with the material.

## Features

- **Interactive Learning**: Students receive instant, guided feedback from an LLM.
- **Easy Assignment Creation**: Instructors can generate assignments from a simple JSON file via the command line.
- **Multiple Views**: Assignments can be run in a classic Jupyter Notebook or served as a clean web application using Voila.
- **Secure Automated Grading**: A command-line script grades all student submissions against a master assignment file, preventing tampering.
- **Simple Workflow**: A `Makefile` automates all common commands.

## Setup

1.  **Clone the repository:** `git clone https://github.com/junli-cuny/Socrates.git && cd Socrates`
2.  **Install dependencies:** `make install`
3.  **Set up environment variables:** Create a `.env` file and add your `OPENAI_API_KEY`. An `.env.example` template is provided.
4.  **Manage the Student Roster (Optional)**

To use the student verification feature, edit the `assignment/whitelist.json` file. This file acts as a central roster for all assignments. Add the unique passcodes for your students to the `passcodes` list.

*See the section below for an explanation of how passcodes work.*

## The Passcode Verification System

This project uses a simple, self-contained verification system to authorize students.

#### What is a Passcode?
A passcode is a unique string created by joining a student's ID number with their first name, with no spaces. The name is case-sensitive.

-   **Format:** `[StudentID][FirstName]`
-   **Example:** If a student's ID is `0572222` and their name is `Jun`, the passcode is `0572222Jun`.

#### How it Works
1.  **Roster:** The instructor maintains the list of valid passcodes in `assignment/whitelist.json`.
2.  **Embedding:** When an assignment is created, this list is embedded into a code cell in the Jupyter Notebook.
3.  **Verification:** The student enters their passcode in the notebook. The code checks if it exists in the embedded list.
4.  **Authorization:** If the passcode is valid, the "Test" and "Submit" buttons are enabled.

#### Important Note on Security
This is a lightweight authorization system designed for classroom convenience, not for high-security applications. A savvy user could inspect the notebook's source code to view the embedded list of passcodes. It serves as an effective deterrent and a simple way to link submissions to students.

## Quickstart with Makefile

A `Makefile` automates all common commands.

-   `make install`: Installs Python dependencies.
-   `make create FILE=<path>`: Creates an assignment notebook.
    -   *Example:* `make create FILE=src/example_question_file.json`
-   `make run`: Starts the classic Jupyter Notebook server.
-   `make serve NOTEBOOK=<path>`: Serves a notebook as a web app.
    -   *Example:* `make serve NOTEBOOK=result/example_question_file.ipynb`
-   `make grade ASSIGNMENT=<path>`: Grades all submissions against a master file.
    -   *Example:* `make grade ASSIGNMENT=src/example_question_file.json`
-   `make report`: Generate an HTML report from the last run
-   `make clean`: Removes all generated files.

## Workflow 

This is the simplest way to deliver an assignment. The instructor runs the server locally, and students access it via a single, secure URL. No installation is required for students.

### Instructor Workflow

**Step 1: Download ngrok**

`ngrok` is a free tool that creates a secure public URL for your local server.

1.  Go to the [ngrok download page](https://ngrok.com/download).
2.  Download the version for your operating system (Windows, macOS, Linux).
3.  Unzip the downloaded file. This will give you a single `ngrok` executable file. Place it in your project directory for easy access.

**Step 2: Create the Assignment**

From your terminal in the project directory, run the `make create` command.
```bash
# This creates result/integer_questions.ipynb
make create FILE=assignment/[question_file.json]
```

**Step 3: Start the Assignment Server (Terminal 1)**

Serve the newly created notebook using the `make serve` command. This will start a local server, typically on port `8866`. **Keep this terminal running.**
```bash
make serve NOTEBOOK=result/integer_questions.ipynb
```
You will see output indicating that the Voila server is running on `localhost:8866`.

**Step 4: Start the ngrok Tunnel (Terminal 2)**

Open a **new terminal window** and navigate to your project directory. Run the `ngrok` command, telling it to expose port `8866`.
```bash
# On macOS/Linux
./ngrok http 8866

# On Windows
.\ngrok.exe http 8866
```
`ngrok` will start and display a screen with a public URL, which will look something like this:
`Forwarding https://random-string-of-characters.ngrok-free.app -> http://localhost:8866`

**Step 5: Share the URL with Students**

Copy the secure `https` URL (e.g., `https://random-string-of-characters.ngrok-free.app`) and share it with your students. This is the only thing they need.

**Step 6: Grade Submissions**

After students have completed the assignment, you will find their `answers_{userID}.json` files saved directly into your `result/` folder.
1.  Stop the servers (`Ctrl+C` in both terminals).
2.  Run the grading command:
    ```bash
    make grade ASSIGNMENT=assignment/[question_file.json]
    ```
3.  Open the generated `grading_report.html` file in your browser to see the results.

---

### Student Workflow

The student experience is now incredibly simple:

1.  **Receive the URL** from the instructor (e.g., `https://random-string-of-characters.ngrok-free.app`).
2.  **Open the URL** in any web browser. The interactive assignment will load directly.
3.  **Complete the assignment:**
    *   Enter their passcode (StudentID + FirstName) and click **Verify**.
    *   Answer the questions and use the **Test** button for feedback.
    *   Click the final **Submit Assignment** button.

When a student clicks "Submit," their `answers.json` file is saved directly to the instructor's computer in the `result/` folder, ready for grading.

---

## Advanced / Local Development Workflow

This workflow is for instructors who want to run everything on their own machine for testing, or for students who have cloned the repository and want to complete an assignment locally.

### 1. Instructor: Create an Assignment
```bash
make create FILE=assignment/[question_file.json]
```

### 2. Student: Complete the Assignment Locally
```bash
# Option A: Serve as a Web App
make serve NOTEBOOK=result/[question_file.ipynb]

# Option B: Use Jupyter Notebook
make run
```
After submitting, the `answers_{userID}.json` file will be created in the `result/` folder.

### 3. Instructor: Grade Submissions
```bash
make grade ASSIGNMENT=assignment/[question_file.json]
```
Open `grading_report.html` to review the results.


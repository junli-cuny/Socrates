# src/generate_report.py

import json
from pathlib import Path

def generate_html_report(results_path, output_path):
    """
    Reads a grading_results.json file and generates a styled HTML report.
    """
    try:
        with open(results_path, 'r', encoding='utf-8') as f:
            grading_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Grading results file not found at {results_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {results_path}. Make sure it's a valid JSON file.")
        return

    # --- HTML and CSS Styling ---
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grading Report</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; background-color: #f8f9fa; }
            .container { max-width: 900px; margin: 20px auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
            h1 { color: #2c3e50; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 40px; }
            .student-card { border: 1px solid #ddd; border-radius: 8px; margin-bottom: 25px; overflow: hidden; }
            .student-header { background-color: #3498db; color: white; padding: 12px 15px; font-size: 1.2em; font-weight: bold; }
            .question-block { padding: 15px; border-bottom: 1px solid #eee; }
            .question-block:last-child { border-bottom: none; }
            .question-title { font-weight: bold; color: #2980b9; }
            .status { font-weight: bold; padding: 4px 8px; border-radius: 4px; color: white; display: inline-block; margin-left: 10px;}
            .status-accepted { background-color: #2ecc71; }
            .status-failed { background-color: #e74c3c; }
            .details { margin-top: 10px; }
            .details strong { color: #555; }
            pre { background-color: #ecf0f1; padding: 12px; border-radius: 5px; white-space: pre-wrap; word-wrap: break-word; font-family: "Courier New", Courier, monospace; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Socrates Grading Report</h1>
    """

    # --- Generate Content for Each Student ---
    for student_file, results in grading_data.items():
        # Clean up student ID from filename
        student_id = student_file.replace("answers_", "").replace(".json", "")

        html_content += f"""
        <div class="student-card">
            <div class="student-header">Student: {student_id}</div>
        """

        # Sort questions by ID (q1, q2, etc.)
        sorted_questions = sorted(results.keys())

        for q_id in sorted_questions:
            q_data = results[q_id]
            avg_rate = q_data.get('avg_rates', 0)
            status_class = "status-accepted" if avg_rate >= 0.5 else "status-failed"
            status_text = "Accepted" if avg_rate >= 0.5 else "Failed"

            html_content += f"""
            <div class="question-block">
                <span class="question-title">Question {q_id.replace('q', '')}</span>
                <span class="status {status_class}">{status_text}</span>
                <div class="details">
                    <strong>Success Rate:</strong> {avg_rate:.2f}<br>
                    <strong>Grading Time:</strong> {q_data.get('time', 0):.2f} seconds
                </div>
            </div>
            """

    html_content += """
        </div>
    </body>
    </html>
    """

    # --- Write the HTML file ---
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Success! Report generated at: {output_path}")


if __name__ == "__main__":
    # Define paths relative to the project structure
    # This script is in 'src/', so we go up one level to the project root.
    project_root = Path(__file__).parent.parent
    results_file = project_root / "grading_results.json"
    report_file = project_root / "grading_report.html" # Save report in the root directory for easy access

    generate_html_report(results_file, report_file)

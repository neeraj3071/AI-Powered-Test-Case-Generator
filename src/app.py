
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Notes per testing framework
framework_notes = {
    "pytest": """
- Use `pytest` syntax (no unittest module).
- Function names should start with `test_`.
- Use `assert` statements.
- Use fixtures for setup if necessary.
""",
    "doctest": """
- Add inline tests in docstrings using proper doctest format.
- Include examples covering various scenarios.
""",
    "junit": """
- Use JUnit 5 (`@Test` annotations).
- Use assertions like `assertEquals`, `assertTrue`, etc.
- Use meaningful method names: `testMethodName_scenario`.
"""
}

# Common additional testing instructions
additional_notes = """
- Cover:
  - Normal cases (expected inputs)
  - Edge cases (boundaries, zero, empty, etc.)
  - Invalid cases (exceptions, incorrect inputs)
- Include explanatory comments for each test.
- Ensure code is clean, syntactically correct, and ready to run.
"""

# Detect programming language using OpenAI
def detect_language(code: str):
    prompt = f"""
Analyze the following code snippet and accurately identify the programming language.

Code:
{code}

Only respond with the language name, without any additional text.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Language detection error:", e)
        return "Unknown"

# Generate test cases from code and framework
def generate_test_cases(code: str, language: str, framework: str):
    prompt = f"""
You are an expert {language} developer and unit testing specialist.

Write high-quality unit tests for the code below using the {framework} framework.

Code to Test:
```{language}
{code}
```

Testing Instructions:
{framework_notes.get(framework.lower(), '')}

{additional_notes}

Output ONLY the test code — no markdown, no explanations, no extra text.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Test generation error:", e)
        return f"# Error generating test cases: {str(e)}"

# Endpoint: Generate initial test cases
@app.route("/generate_tests", methods=["POST"])
def generate_tests():
    try:
        data = request.get_json()
        input_code = data.get("code")
        framework = data.get("framework", "pytest")

        if not input_code:
            return jsonify({"error": "No code provided"}), 400

        detected_language = detect_language(input_code)
        test_cases = generate_test_cases(input_code, detected_language, framework)

        return jsonify({
            "detected_language": detected_language,
            "generated_tests": test_cases
        })

    except Exception as e:
        print("Server error:", e)
        return jsonify({"error": str(e)}), 500

# Endpoint: Regenerate test cases using feedback
@app.route("/regenerate_tests_with_feedback", methods=["POST"])
def regenerate_with_feedback():
    try:
        data = request.get_json()
        code = data.get("code")
        framework = data.get("framework")
        feedback = data.get("feedback", "")
        language = detect_language(code)

        prompt = f"""
You are an expert {language} developer and unit testing specialist.

Original Code:
```{language}
{code}
```

User Feedback:
"{feedback}"

Regenerate high-quality test cases using the {framework} framework, and make sure to incorporate the user's feedback above.

Testing Instructions:
{framework_notes.get(framework.lower(), '')}

{additional_notes}

Output ONLY the test code — no markdown, no extra text.
"""
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )

        return jsonify({
            "generated_tests": response.choices[0].message.content.strip()
        })
    except Exception as e:
        print("Regeneration error:", e)
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

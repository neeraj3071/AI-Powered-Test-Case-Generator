from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Securely access OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Flask setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Detect programming language
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

# Generate test cases with framework-specific instructions
def generate_test_cases(code: str, language: str, framework: str):
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

    additional_notes = """
- Cover:
  - Normal cases (expected inputs)
  - Edge cases (boundaries, zero, empty, etc.)
  - Invalid cases (exceptions, incorrect inputs)
- Include explanatory comments for each test.
- Ensure code is clean, syntactically correct, and ready to run.
"""

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

# API endpoint
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

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

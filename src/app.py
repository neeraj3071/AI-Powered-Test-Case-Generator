from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_language(code: str):
    prompt = f"""
    Identify the programming language of this code snippet:

    Code:
    {code}

    Only reply with the language name.
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
        print(f"Language detection error: {e}")
        return "Unknown"

def generate_test_cases(code: str, language: str, framework: str):
    prompt = f"""
    Generate unit tests for the following {language} code using the {framework} testing framework.

    ```{language}
    {code}
    ```

    Guidelines:
    - Follow best practices for {framework}.
    - Cover standard, edge, and invalid cases.
    - Use mocks/stubs if needed.
    - Include comments explaining the test cases.
    - Output complete, runnable test code.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Test case generation error: {e}")
        return f"Error: {str(e)}"

@app.route("/generate_tests", methods=["POST"])
def generate_tests():
    data = request.get_json()
    code = data.get("code")
    framework = data.get("framework", "pytest")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    language = detect_language(code)
    tests = generate_test_cases(code, language, framework)

    return jsonify({
        "detected_language": language,
        "generated_tests": tests
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

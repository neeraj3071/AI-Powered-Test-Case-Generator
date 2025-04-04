import os
import json
import requests
import subprocess

API_URL = "http://127.0.0.1:5000/generate_tests"
SUPPORTED_EXTENSIONS = [".py", ".java"]
FRAMEWORK_MAP = {
    ".py": "pytest",
    ".java": "JUnit"
}

def get_changed_files():
    try:
        # Get files changed in this PR
        output = subprocess.check_output(["git", "diff", "--name-only", "origin/main...HEAD"]).decode()
        return [line.strip() for line in output.split("\n") if line.strip()]
    except subprocess.CalledProcessError:
        return []

def read_file_content(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Could not read {path}: {e}")
        return ""

def send_to_backend(code, framework):
    try:
        response = requests.post(API_URL, json={"code": code, "framework": framework})
        return response.json()
    except Exception as e:
        return {"error": f"API error: {e}"}

def main():
    changed_files = get_changed_files()
    results = []

    for file in changed_files:
        ext = os.path.splitext(file)[1]
        if ext in SUPPORTED_EXTENSIONS:
            print(f"\n📄 Processing {file}...")
            code = read_file_content(file)
            framework = FRAMEWORK_MAP.get(ext, "pytest")

            response = send_to_backend(code, framework)

            result = {
                "file": file,
                "framework": framework,
                "language": response.get("detected_language", "Unknown"),
                "tests": response.get("generated_tests", "Failed to generate.")
            }

            results.append(result)

    # Output all results
    with open("generated_tests_report.md", "w", encoding="utf-8") as f:
        for r in results:
            f.write(f"### {r['file']} ({r['framework']})\n")
            f.write(f"**Detected Language**: {r['language']}\n\n")
            f.write("```{}\n{}\n```\n\n".format(
                "python" if r["framework"] in ["pytest", "DocTest"] else "java",
                r["tests"]
            ))

    print("✅ Test cases written to generated_tests_report.md")

if __name__ == "__main__":
    main()

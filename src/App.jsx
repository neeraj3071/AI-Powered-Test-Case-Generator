import React, { useState, useCallback } from "react";
import './App.css';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

function App() {
  const [inputCode, setInputCode] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  const [generatedTestCases, setGeneratedTestCases] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedFramework, setSelectedFramework] = useState('pytest');
  const [feedback, setFeedback] = useState('');

  const handleGenerateClick = useCallback(async () => {
    if (!inputCode.trim()) {
      setError("Please enter some code to analyze.");
      return;
    }

    const isJava = /public\s+class|System\.out\.println|void\s+main/.test(inputCode);
    const isPython = /def\s+\w+\s*\(|print\(|import\s+\w+/.test(inputCode);

    if (isJava && selectedFramework !== 'junit') {
      setError("⚠️ Java code detected. Please select JUnit as the testing framework.");
      return;
    }

    if (isPython && selectedFramework === 'junit') {
      setError("⚠️ Python code detected. JUnit is not compatible. Please select Pytest or Doctest.");
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch("http://127.0.0.1:5000/generate_tests", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: inputCode,
          framework: selectedFramework
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to generate test cases: ${response.statusText}`);
      }

      const data = await response.json();

      setDetectedLanguage(data.detected_language || "Unknown");
      setGeneratedTestCases(data.generated_tests || "No test cases generated.");
    } catch (error) {
      console.error("Error:", error);
      setError("An error occurred. Please try again later.");
    } finally {
      setLoading(false);
    }
  }, [inputCode, selectedFramework]);

  const handleFeedbackSubmit = async () => {
    if (!feedback.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch("http://127.0.0.1:5000/regenerate_tests_with_feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: inputCode,
          framework: selectedFramework,
          feedback: feedback
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to regenerate: ${response.statusText}`);
      }

      const data = await response.json();
      setGeneratedTestCases(data.generated_tests || "No updated test cases generated.");
    } catch (error) {
      setError("Error during feedback regeneration: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (generatedTestCases) {
      navigator.clipboard.writeText(generatedTestCases);
      alert("✅ Test cases copied to clipboard!");
    }
  };

  const handleDownload = () => {
    if (generatedTestCases) {
      let extension = ".txt";

      if (selectedFramework === "junit") extension = ".java";
      if (["pytest", "doctest"].includes(selectedFramework)) extension = ".py";

      const file = new Blob([generatedTestCases], { type: "text/plain" });
      const element = document.createElement("a");
      element.href = URL.createObjectURL(file);
      element.download = `generated_test_cases${extension}`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }
  };

  return (
    <div className="App">
      <div className="left-side">
        <h1>Unit Test Case Generator</h1>
        <p className="subtitle">Paste your code below to automatically generate unit test cases.</p>

        <textarea
          placeholder="Paste your code here..."
          value={inputCode}
          onChange={(e) => setInputCode(e.target.value)}
          rows="10"
        ></textarea>

        <label htmlFor="test-framework" style={{ marginTop: '15px', fontWeight: 'bold' }}>Choose Testing Framework:</label>
        <select
          id="test-framework"
          value={selectedFramework}
          onChange={(e) => setSelectedFramework(e.target.value)}
        >
          <option value="pytest">Pytest (Python)</option>
          <option value="junit">JUnit (Java)</option>
          <option value="doctest">Doctest (Python)</option>
        </select>

        <button onClick={handleGenerateClick} disabled={loading} className={loading ? "analyze-button loading" : "analyze-button"}>
          {loading ? <div className="spinner"></div> : "Generate Test Cases"}
        </button>

        {error && <p className="error">{error}</p>}

        <div className="detected-smell">
          <h2>Detected Language</h2>
          <div className="output-content">
            {detectedLanguage || "Language will be detected when you generate test cases."}
          </div>
        </div>
      </div>

      <div className="right-side">
        <h2>Generated Test Cases</h2>
        {generatedTestCases ? (
          <SyntaxHighlighter language={selectedFramework === 'junit' ? 'java' : 'python'} style={oneDark}>
            {generatedTestCases}
          </SyntaxHighlighter>
        ) : (
          <div className="output-content">
            Test cases will appear here after generation.
          </div>
        )}

        {generatedTestCases && (
          <>
            <div style={{ marginTop: "1rem", display: "flex", gap: "10px" }}>
              <button onClick={handleCopy}>📋 Copy to Clipboard</button>
              <button onClick={handleDownload}>📥 Download as File</button>
            </div>

            <div className="feedback-section" style={{ marginTop: "20px" }}>
              <h3>Not happy with the test cases?</h3>
              <textarea
                placeholder="Enter your feedback here (e.g., add more edge cases, use mocks)..."
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                rows="4"
                style={{
                  width: "100%",
                  padding: "10px",
                  marginTop: "10px",
                  fontSize: "14px",
                  borderRadius: "6px",
                  border: "1px solid #ccc",
                }}
              />
              <button onClick={handleFeedbackSubmit} style={{ marginTop: "10px" }}>
                💬 Submit Feedback & Regenerate
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;

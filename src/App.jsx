import React, { useState, useCallback } from "react";
import './App.css';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

function App() {
  const [inputCode, setInputCode] = useState('');
  const [framework, setFramework] = useState('pytest');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  const [generatedTestCases, setGeneratedTestCases] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerateClick = useCallback(async () => {
    if (!inputCode.trim()) {
      setError("Please enter some code to analyze.");
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch("http://127.0.0.1:5000/generate_tests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: inputCode, framework })
      });

      const data = await response.json();

      if (response.ok && data.detected_language && data.generated_tests) {
        setDetectedLanguage(data.detected_language);
        setGeneratedTestCases(data.generated_tests);
      } else {
        setDetectedLanguage("Unknown");
        setGeneratedTestCases("No test cases generated.");
        setError(data.error || "Unexpected error.");
      }

    } catch (error) {
      console.error("Fetch error:", error);
      setError("Server error: " + error.message);
    } finally {
      setLoading(false);
    }
  }, [inputCode, framework]);

  return (
    <div className="App">
      <div className="left-side">
        <h1>AI-Powered Unit Test Generator</h1>
        <textarea
          placeholder="Paste your code here..."
          value={inputCode}
          onChange={(e) => setInputCode(e.target.value)}
          rows="10"
        />
        <select value={framework} onChange={(e) => setFramework(e.target.value)}>
          <option value="pytest">pytest (Python)</option>
          <option value="DocTest">DocTest (Python)</option>
          <option value="JUnit">JUnit (Java)</option>
        </select>
        <button onClick={handleGenerateClick} disabled={loading}>
          {loading ? "Generating..." : "Generate Test Cases"}
        </button>
        {error && <p className="error">{error}</p>}
        <h2>Detected Language:</h2>
        <div>{detectedLanguage}</div>
      </div>

      <div className="right-side">
        <h2>Generated Test Cases</h2>
        {generatedTestCases ? (
          <SyntaxHighlighter language="python" style={oneDark}>
            {generatedTestCases}
          </SyntaxHighlighter>
        ) : (
          <p>Test cases will appear here.</p>
        )}
      </div>
    </div>
  );
}

export default App;

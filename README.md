# 🧪 AI-Powered Test Case Generator for Unit Testing

This project is an **AI-powered tool** that automatically generates unit test cases for your source code using OpenAI’s language model. It supports multiple programming languages and testing frameworks, and provides a smooth developer experience with a user-friendly frontend built using **React + Vite**, and a powerful **Flask backend**.

## 🚀 Features

- 🔍 **Automatic Language Detection**: Detects the programming language of your code.
- ⚙️ **Framework-Specific Test Generation**: Supports `pytest`, `JUnit`, and `doctest`.
- 📂 **Separate File Generation**: Test cases are saved in individual files based on class names.
- 🔁 **Real-time Feedback Loop** *(Coming Soon)*: Developers can rate and regenerate test cases.
- 🧠 **Interactive Chat Support** *(Planned)*: Regenerate test cases based on developer feedback.
- ✅ **CI/CD Integration** *(Planned)*: Auto-generate test cases on every pull request.
- 📊 **Reports**: Automatically generate markdown reports for all created test cases.

---

## 🏗️ Project Structure

```
AI-Powered-Test-Case-Generator-for-Unit-Testing/
├── src/                         # Contains both frontend (React) and backend (Flask) code
├── generated_unit_test_cases/  # Auto-generated test files
├── reports/                     # Markdown reports
├── .env                         # API keys and environment variables
└── README.md                    # Project documentation
```

---

## 🛠️ Tech Stack

- **Frontend**: React.js (Vite), Tailwind CSS
- **Backend**: Flask, OpenAI API
- **Others**: Python, Node.js, GitHub Actions

---

## 📥 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/manankathrecha/AI-Powered-Test-Case-Generator-for-Unit-Testing.git
cd AI-Powered-Test-Case-Generator-for-Unit-Testing
```

---

### 2️⃣ Backend Setup (Flask)

#### 📌 Prerequisites
- Python 3.8+
- pip
- Create a `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_key_here
```

#### 🧪 Create and activate a virtual environment

```bash
cd src
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### ▶️ Run the backend server

```bash
python app.py
```

The Flask server should start on `http://localhost:5000`.

---

### 3️⃣ Frontend Setup (React + Vite)

#### 📌 Prerequisites
- Node.js (v18+ recommended)
- npm

```bash
cd src
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`.

---

## 💡 How It Works

1. Paste your code into the frontend text box.
2. The app detects the programming language.
3. You choose a supported test framework (based on language).
4. OpenAI API generates corresponding unit test cases.
5. The generated test is:
   - Saved in `generated_unit_test_cases/`
   - Reported in `reports/generated_tests_report.md`

---

## 🧪 Example Output

For a Java class `Calculator`, the tool generates a `CalculatorTest.java` file like:

```java
@Test
public void testAdd_positiveNumbers() {
    int result = Calculator.add(3, 5);
    assertEquals(8, result);
}
```

---

## 🧰 Future Enhancements

- 🌐 Feedback chat interface to regenerate better tests
- 🧪 More framework support: `Mocha`, `RSpec`, `GoTest`, etc.
- 🔁 GitHub Action integration for test automation
- 🗂️ Downloadable zip of all test cases

---

## 🤝 Contributing

We welcome contributions! Feel free to:
- Create issues for bugs or features
- Submit pull requests
- Suggest UI/UX improvements

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🔗 Related Links

- 🔗 [OpenAI API](https://platform.openai.com/docs/)
- 🔗 [Flask Documentation](https://flask.palletsprojects.com/)
- 🔗 [React Documentation](https://reactjs.org/)

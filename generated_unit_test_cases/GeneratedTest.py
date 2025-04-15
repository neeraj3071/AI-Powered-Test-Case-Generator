```Python
import pytest
import os
from unittest.mock import patch, MagicMock
from your_module import get_changed_files, read_file_content, send_to_backend, extract_class_name, main

# Test get_changed_files function
def test_get_changed_files():
    with patch("subprocess.check_output") as mock_output:
        mock_output.return_value = b"file1.py\nfile2.java\n"
        files = get_changed_files()
        assert files == ["file1.py", "file2.java"]

# Test read_file_content function
def test_read_file_content(tmpdir):
    file = tmpdir.join("test.py")
    file.write("print('Hello, World!')")
    assert read_file_content(file) == "print('Hello, World!')"

# Test send_to_backend function
def test_send_to_backend():
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"detected_language": "python", "generated_tests": "test_code"}
        mock_post.return_value = mock_response
        response = send_to_backend("print('Hello, World!')", "pytest")
        assert response == {"detected_language": "python", "generated_tests": "test_code"}

# Test extract_class_name function
def test_extract_class_name():
    python_code = "class TestClass:\n    pass"
    java_code = "public class TestClass {}"
    assert extract_class_name(python_code, "python") == "TestClass"
    assert extract_class_name(java_code, "java") == "TestClass"

# Test main function
def test_main(tmpdir):
    with patch("subprocess.check_output") as mock_output, patch("requests.post") as mock_post, patch("builtins.open", new_callable=pytest.mock.mock_open):
        # Mock subprocess.check_output
        mock_output.return_value = b"file1.py\nfile2.java\n"
        # Mock requests.post
        mock_response = MagicMock()
        mock_response.json.return_value = {"detected_language": "python", "generated_tests": "test_code"}
        mock_post.return_value = mock_response
        # Mock open
        mock_file = MagicMock()
        mock_file.write.return_value = None
        mock_file.read.return_value = "- `file1.py` → **TestClassTest.py** (python, pytest)\n- `file2.java` → **TestClassTest.java** (java, JUnit)\n"
        open.return_value = mock_file
        # Change working directory to temporary directory
        os.chdir(tmpdir)
        # Run main function
        main()
        # Check if the generated test cases and report are created
        assert os.path.exists("generated_unit_test_cases/TestClassTest.py")
        assert os.path.exists("generated_unit_test_cases/TestClassTest.java")
        assert os.path.exists("generated_tests_report.md")
```
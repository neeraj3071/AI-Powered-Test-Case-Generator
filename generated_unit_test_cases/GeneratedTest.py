```Python
import pytest
import os
import subprocess
from unittest.mock import patch, MagicMock
from your_module import get_changed_files, read_file_content, send_to_backend, extract_class_name, main

# Test get_changed_files function
def test_get_changed_files():
    with patch('subprocess.check_output') as mock_output:
        mock_output.return_value = b"file1.py\nfile2.java\n"
        assert get_changed_files() == ['file1.py', 'file2.java']

def test_get_changed_files_empty():
    with patch('subprocess.check_output') as mock_output:
        mock_output.return_value = b""
        assert get_changed_files() == []

def test_get_changed_files_exception():
    with patch('subprocess.check_output', side_effect=Exception):
        assert get_changed_files() == []

# Test read_file_content function
def test_read_file_content():
    with patch('builtins.open', new_callable=MagicMock):
        assert read_file_content('path') == ''

def test_read_file_content_exception():
    with patch('builtins.open', side_effect=Exception):
        assert read_file_content('path') == ''

# Test send_to_backend function
def test_send_to_backend():
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"detected_language": "python", "generated_tests": "test_code"}
        assert send_to_backend('code', 'pytest') == {"detected_language": "python", "generated_tests": "test_code"}

def test_send_to_backend_exception():
    with patch('requests.post', side_effect=Exception):
        assert send_to_backend('code', 'pytest') == {"error": "API error: "}

# Test extract_class_name function
def test_extract_class_name_python():
    assert extract_class_name('class TestClass:', 'python') == 'TestClass'

def test_extract_class_name_java():
    assert extract_class_name('public class TestClass {', 'java') == 'TestClass'

def test_extract_class_name_no_match():
    assert extract_class_name('no class here', 'python') == 'Generated'

# Test main function
@patch('your_module.get_changed_files')
@patch('your_module.read_file_content')
@patch('your_module.send_to_backend')
@patch('your_module.extract_class_name')
@patch('os.makedirs')
@patch('builtins.open')
def test_main(mock_open, mock_makedirs, mock_extract_class_name, mock_send_to_backend, mock_read_file_content, mock_get_changed_files):
    mock_get_changed_files.return_value = ['file1.py']
    mock_read_file_content.return_value = 'class TestClass:'
    mock_send_to_backend.return_value = {"detected_language": "python", "generated_tests": "test_code"}
    mock_extract_class_name.return_value = 'TestClass'
    main()
    mock_open.assert_called_with('generated_unit_test_cases/TestClassTest.py', 'w', encoding='utf-8')
```
This test code covers the main functions in the provided code. It tests both the normal and exceptional cases. It uses Python's built-in `unittest.mock` library to mock the behavior of external dependencies like `subprocess.check_output`, `requests.post`, and `open` function.
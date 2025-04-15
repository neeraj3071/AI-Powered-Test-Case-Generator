```Python
import pytest
import os
import json
import requests
import subprocess
import re
from unittest.mock import patch, Mock

# Import the module to test
import my_module

def test_get_changed_files():
    # Mock subprocess.check_output to return a list of files
    with patch('subprocess.check_output') as mock_check_output:
        mock_check_output.return_value = b'file1.py\nfile2.java\n'
        files = my_module.get_changed_files()
        assert files == ['file1.py', 'file2.java']

    # Test the exception case
    with patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'cmd')):
        files = my_module.get_changed_files()
        assert files == []

def test_read_file_content():
    # Mock open to return a string
    with patch('builtins.open', new_callable=Mock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = 'file content'
        content = my_module.read_file_content('path')
        assert content == 'file content'

    # Test the exception case
    with patch('builtins.open', side_effect=Exception('error')):
        content = my_module.read_file_content('path')
        assert content == ''

def test_send_to_backend():
    # Mock requests.post to return a json response
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'response': 'success'}
        response = my_module.send_to_backend('code', 'pytest')
        assert response == {'response': 'success'}

    # Test the exception case
    with patch('requests.post', side_effect=Exception('error')):
        response = my_module.send_to_backend('code', 'pytest')
        assert response == {'error': 'API error: error'}

def test_extract_class_name():
    # Test Python code
    code = 'class MyClass:'
    class_name = my_module.extract_class_name(code, 'Python')
    assert class_name == 'MyClass'

    # Test Java code
    code = 'public class MyClass {}'
    class_name = my_module.extract_class_name(code, 'Java')
    assert class_name == 'MyClass'

    # Test unknown language
    code = 'class MyClass:'
    class_name = my_module.extract_class_name(code, 'Unknown')
    assert class_name == 'Generated'

def test_main():
    # Mock the functions called in main to test the flow
    with patch('my_module.get_changed_files') as mock_get_files, \
         patch('my_module.read_file_content') as mock_read_file, \
         patch('my_module.send_to_backend') as mock_send_to_backend, \
         patch('my_module.extract_class_name') as mock_extract_class, \
         patch('builtins.open', new_callable=Mock) as mock_open:

        mock_get_files.return_value = ['file1.py']
        mock_read_file.return_value = 'class MyClass:'
        mock_send_to_backend.return_value = {'detected_language': 'Python', 'generated_tests': 'test code'}
        mock_extract_class.return_value = 'MyClass'

        my_module.main()

        # Check the calls to the mocked functions
        mock_get_files.assert_called_once()
        mock_read_file.assert_called_once_with('file1.py')
        mock_send_to_backend.assert_called_once_with('class MyClass:', 'pytest')
        mock_extract_class.assert_called_once_with('class MyClass:', 'Python')

        # Check the file write calls
        mock_open.assert_any_call(os.path.join('generated_unit_test_cases', 'MyClassTest.py'), 'w', encoding='utf-8')
        mock_open.assert_any_call('generated_tests_report.md', 'w', encoding='utf-8')
```
```Python
import pytest
import os
import json
import requests
import subprocess
import re
from unittest.mock import patch, Mock

# Import the module to test
import module_to_test

# Test get_changed_files function
def test_get_changed_files():
    with patch('subprocess.check_output') as mocked_check_output:
        mocked_check_output.return_value = b'test.py\n'
        files = module_to_test.get_changed_files()
        assert files == ['test.py']

# Test read_file_content function
def test_read_file_content():
    with patch('builtins.open', new_callable=Mock) as mocked_open:
        mocked_open.return_value.__enter__.return_value.read.return_value = 'print("Hello, World!")'
        content = module_to_test.read_file_content('test.py')
        assert content == 'print("Hello, World!")'

# Test send_to_backend function
def test_send_to_backend():
    with patch('requests.post') as mocked_post:
        mocked_post.return_value.json.return_value = {'detected_language': 'python', 'generated_tests': 'def test_hello():\n    assert True'}
        response = module_to_test.send_to_backend('print("Hello, World!")', 'pytest')
        assert response == {'detected_language': 'python', 'generated_tests': 'def test_hello():\n    assert True'}

# Test extract_class_name function
def test_extract_class_name():
    class_name = module_to_test.extract_class_name('class TestClass:', 'python')
    assert class_name == 'TestClass'

# Test main function
def test_main():
    with patch('module_to_test.get_changed_files') as mocked_get_changed_files, \
         patch('module_to_test.read_file_content') as mocked_read_file_content, \
         patch('module_to_test.send_to_backend') as mocked_send_to_backend, \
         patch('module_to_test.extract_class_name') as mocked_extract_class_name, \
         patch('builtins.open', new_callable=Mock) as mocked_open, \
         patch('os.makedirs') as mocked_makedirs:

        mocked_get_changed_files.return_value = ['test.py']
        mocked_read_file_content.return_value = 'class TestClass:\n    def hello(self):\n        print("Hello, World!")'
        mocked_send_to_backend.return_value = {'detected_language': 'python', 'generated_tests': 'def test_hello():\n    assert True'}
        mocked_extract_class_name.return_value = 'TestClass'

        module_to_test.main()

        mocked_open.assert_called_with(os.path.join('generated_unit_test_cases', 'TestClassTest.py'), 'w', encoding='utf-8')
        mocked_makedirs.assert_called_with('generated_unit_test_cases', exist_ok=True)
```
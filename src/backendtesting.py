
import unittest
import json
from app import app, detect_language, generate_test_cases # Assuming the code is in a file named app.py

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_detect_language(self):
        code = 'print("Hello, World!")'
        result = detect_language(code)
        self.assertEqual(result, 'Python')

        code = 'console.log("Hello, World!");'
        result = detect_language(code)
        self.assertEqual(result, 'JavaScript')

        code = 'unknown language code'
        result = detect_language(code)
        self.assertEqual(result, 'Unknown')

    def test_generate_test_cases(self):
        code = 'def add(a, b): return a + b'
        language = 'Python'
        result = generate_test_cases(code, language)
        self.assertIsNotNone(result)

        code = 'function add(a, b) { return a + b; }'
        language = 'JavaScript'
        result = generate_test_cases(code, language)
        self.assertIsNotNone(result)

    def test_generate_tests_endpoint(self):
        response = self.app.post('/generate_tests', data=json.dumps({"code": 'print("Hello, World!")'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data["detected_language"], 'Python')
        self.assertIsNotNone(data["generated_tests"])

        response = self.app.post('/generate_tests', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
if __name__ == '__main__':
    unittest.main()

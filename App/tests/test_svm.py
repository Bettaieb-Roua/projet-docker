# test_svm.py
import unittest
import os
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from App import app

class TestSVMApi(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_svm_valid_file(self):
        # Ensure test file exists
        test_file_path = os.path.join(os.path.dirname(__file__), 'test.wav')
        
        # Debug: Print file existence
        print(f"Test file path: {test_file_path}")
        print(f"Test file exists: {os.path.exists(test_file_path)}")
        
        with open(test_file_path, 'rb') as file:
            rv = self.app.post('/uploaderSVM', data={'file': (file, 'test.wav')}, content_type='multipart/form-data')
            
            # Debug: Print response details
            print(f"Response status: {rv.status_code}")
            print(f"Response data: {rv.get_json()}")
            
            self.assertEqual(rv.status_code, 200)
            data = rv.get_json()
            self.assertIn('result', data)

    def test_svm_invalid_file_type(self):
        with open(os.path.join(os.path.dirname(__file__), 'test.png'), 'rb') as file:
            rv = self.app.post('/uploaderSVM', data={'file': (file, 'test.png')}, content_type='multipart/form-data')
            self.assertEqual(rv.status_code, 400)
            data = rv.get_json()
            self.assertIn('error', data)

    def test_svm_no_file(self):
        rv = self.app.post('/uploaderSVM')
        self.assertEqual(rv.status_code, 400)
        data = rv.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
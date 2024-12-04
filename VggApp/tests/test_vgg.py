import unittest
import os
import requests
import sys
from App import app

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

class TestVGGApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://localhost:8082'
        cls.test_image_path = os.path.join(os.path.dirname(__file__), 'test.png')

    def test_vgg_home_route(self):
        response = requests.get(f'{self.base_url}/vgg')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)

    def test_vgg_valid_image_upload(self):
        self.assertTrue(os.path.exists(self.test_image_path), 
                        f"Test image not found at {self.test_image_path}")

        with open(self.test_image_path, 'rb') as image_file:
            response = requests.post(
                f'{self.base_url}/uploaderVGG',
                files={'file': ('test.png', image_file, 'image/png')}
            )

        self.assertEqual(response.status_code, 200)

    def test_vgg_no_file_upload(self):
        response = requests.post(f'{self.base_url}/uploaderVGG')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()

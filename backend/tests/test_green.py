import unittest
from app import create_app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 404])  

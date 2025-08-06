import unittest
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_register_missing_fields(self):
        response = self.client.post('/api/auth/register', json={
            'email': 'test@example.com'

        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required field', response.data) #python -m unittest tests/test_auth.py
import unittest

from server import app 
from model import db, example_data, connect_to_db

class Tests(unittest.TestCase):
    "Tests for site."

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_register_form(self):
        result = self.client.get("/register-form")
        self.assertIn(b"Register Form", result.data)






if __name__ == "__main__":
    unittest.main()
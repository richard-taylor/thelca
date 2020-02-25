import requests
import unittest

class TestBlackBoxDocumentationAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:2207/'

    def test_get_documentation_without_a_token(self):
        response = requests.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertIn('Meeeow', response.text)
        self.assertIn('Server', response.headers)
        self.assertEqual('TheElectricCat/0 X', response.headers['Server'])

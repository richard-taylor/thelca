import requests
import unittest

def jwt():
    return {'Authorization': 'Bearer abcd'}

class TestBlackBoxDocumentationAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'https://localhost:2207/'

    def test_get_documentation_without_a_token(self):
        response = requests.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertIn('Meeeow', response.text)
        self.assertIn('Server', response.headers)
        self.assertEqual('TheElectricCat/0 X', response.headers['Server'])

    def test_help_fails_without_a_token(self):
        response = requests.get(self.url + "help")
        self.assertEqual(401, response.status_code)

    def test_help_succeeds_with_a_token(self):
        response = requests.get(self.url + "help", headers = jwt())
        self.assertEqual(200, response.status_code)
        self.assertIn('The Electric Cat', response.text)

    def test_health_fails_without_a_token(self):
        response = requests.get(self.url + "health")
        self.assertEqual(401, response.status_code)

    def test_health_succeeds_with_a_token(self):
        response = requests.get(self.url + "health", headers = jwt())
        self.assertEqual(200, response.status_code)
        self.assertIn('UP', response.text)

    def test_metrics_fails_without_a_token(self):
        response = requests.get(self.url + "metrics")
        self.assertEqual(401, response.status_code)

    def test_metrics_succeeds_with_a_token(self):
        response = requests.get(self.url + "metrics", headers = jwt())
        self.assertEqual(200, response.status_code)
        self.assertIn('http_responses{code="200"}', response.text)

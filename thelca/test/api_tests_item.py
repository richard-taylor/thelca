import requests
import unittest

class TestBlackBoxItemAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:2207/v1/items'

    def test_get_fails_for_non_item(self):
        response = requests.get(self.url + '/no-such-id')
        self.assertEqual(404, response.status_code)

    def test_post_fails_for_non_json(self):
        response = requests.post(self.url, data = 'not json')
        self.assertEqual(400, response.status_code)
        self.assertIn('The data is not a JSON string', response.text)

    def test_post_fails_with_id(self):
        response = requests.post(self.url, data = '{"id": "fake-id"}')
        self.assertEqual(400, response.status_code)
        self.assertIn('id cannot be set externally', response.text)

    def test_post_fails_with_created_at(self):
        response = requests.post(self.url, data = '{"created_at": "noon"}')
        self.assertEqual(400, response.status_code)
        self.assertIn('created_at cannot be set externally', response.text)

    def test_post_fails_with_created_by(self):
        response = requests.post(self.url, data = '{"created_by": "me"}')
        self.assertEqual(400, response.status_code)
        self.assertIn('created_by cannot be set externally', response.text)

    def test_post_succeeds_for_empty_json(self):
        response = requests.post(self.url, data = '{}')
        self.assertEqual(200, response.status_code)

        json = response.json()
        self.assertIn('id', json)
        self.assertIn('created_at', json)
        self.assertIn('created_by', json)
        self.assertIn('properties', json)

        self.assertIsNotNone(json['id'])
        self.assertIsNotNone(json['created_at'])
        self.assertIsNotNone(json['created_by'])

        self.assertIsNone(json['properties'])

    def test_get_succeeds_for_new_item(self):
        post_response = requests.post(self.url, data = '{"properties": {"a": "b"}}')
        self.assertEqual(200, post_response.status_code)

        new_item = post_response.json()

        get_response = requests.get(self.url + '/' + new_item['id'])
        self.assertEqual(200, get_response.status_code)

        got_item = get_response.json()

        self.assertDictEqual(new_item, got_item)

    def test_post_ignores_extra_fields(self):
        response = requests.post(self.url, data = '''
        {
            "properties": { "type": "BUG", "status": "OPEN" },
            "secret": "you aint seen me, right?"
        }
        ''')
        self.assertEqual(200, response.status_code)

        json = response.json()
        self.assertIn('id', json)
        self.assertIn('created_at', json)
        self.assertIn('created_by', json)
        self.assertIn('properties', json)

        self.assertNotIn('secret', json)

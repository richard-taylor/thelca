import requests
import unittest

from json import dumps

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

    def test_put_fails_for_no_id(self):
        response = requests.put(self.url)
        self.assertEqual(404, response.status_code)

    def test_put_fails_for_non_json(self):
        response = requests.put(self.url + '/1234', data = 'not json')
        self.assertEqual(400, response.status_code)
        self.assertIn('The data is not a JSON string', response.text)

    def test_put_fails_for_non_existent_item(self):
        response = requests.put(self.url + '/1234', data = '{}')
        self.assertEqual(404, response.status_code)

    def test_put_can_change_properties(self):
        post_response = requests.post(self.url, data = '{}')
        self.assertEqual(200, post_response.status_code)

        json = post_response.json()
        json['properties'] = {'type': 'STORY'}

        put_response = requests.put(self.url + '/' + json['id'], data = dumps(json))
        self.assertEqual(200, put_response.status_code)

        get_response = requests.get(self.url + '/' + json['id'])
        self.assertEqual(200, get_response.status_code)

        new_json = get_response.json()

        self.assertDictEqual(new_json, json)

    def test_put_fails_if_empty_item_sent(self):
        post_response = requests.post(self.url, data = '{}')
        self.assertEqual(200, post_response.status_code)

        json = post_response.json()
        true_id = json['id']

        put_response = requests.put(self.url + '/' + true_id, data = '{}')
        self.assertEqual(400, put_response.status_code)
        self.assertIn('id cannot be modified', put_response.text)

    def test_put_fails_if_id_modified(self):
        post_response = requests.post(self.url, data = '{}')
        self.assertEqual(200, post_response.status_code)

        json = post_response.json()
        json['properties'] = {'type': 'STORY'}

        true_id = json['id']
        json['id'] = '1234'

        put_response = requests.put(self.url + '/' + true_id, data = dumps(json))
        self.assertEqual(400, put_response.status_code)
        self.assertIn('id cannot be modified', put_response.text)

    def test_put_fails_if_created_at_modified(self):
        post_response = requests.post(self.url, data = '{}')
        self.assertEqual(200, post_response.status_code)

        json = post_response.json()
        json['properties'] = {'type': 'STORY'}

        true_id = json['id']
        json['created_at'] = 'midnight'

        put_response = requests.put(self.url + '/' + true_id, data = dumps(json))
        self.assertEqual(400, put_response.status_code)
        self.assertIn('created_at cannot be modified', put_response.text)

    def test_put_fails_if_created_by_modified(self):
        post_response = requests.post(self.url, data = '{}')
        self.assertEqual(200, post_response.status_code)

        json = post_response.json()
        json['properties'] = {'type': 'STORY'}

        true_id = json['id']
        json['created_by'] = 'Dr Doom'

        put_response = requests.put(self.url + '/' + true_id, data = dumps(json))
        self.assertEqual(400, put_response.status_code)
        self.assertIn('created_by cannot be modified', put_response.text)

    def test_put_ignores_extra_fields(self):
        post_response = requests.post(self.url, data = '{}')
        self.assertEqual(200, post_response.status_code)

        json = post_response.json()
        json['properties'] = {'type': 'STORY'}
        json['secret'] = 'tell no-one'

        put_response = requests.put(self.url + '/' + json['id'], data = dumps(json))
        self.assertEqual(200, put_response.status_code)
        self.assertNotIn('secret', put_response.json())

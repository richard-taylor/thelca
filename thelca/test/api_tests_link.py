import requests
import unittest

from copy import deepcopy
from json import dumps

def jwt():
    return {'Authorization': 'Bearer abcd'}

class TestBlackBoxLinkAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        url_items = 'http://localhost:2207/v1/items'
        response1 = requests.post(url_items, data = '{}', headers = jwt())
        response2 = requests.post(url_items, data = '{}', headers = jwt())
        cls.item_1_id = response1.json()['id']
        cls.item_2_id = response2.json()['id']

        cls.url = 'http://localhost:2207/v1/links'
        response3 = requests.post(cls.url, headers = jwt(), data = '''
        {{
            "properties": {{
                "type": "BLOCKS"
            }},
            "source": "{0}",
            "target": "{1}"
        }}
        '''.format(cls.item_1_id, cls.item_2_id))
        cls.link = response3.json()

    def test_get_fails_with_unauthorized_if_no_token_sent(self):
        response = requests.get(self.url + '/1234')
        self.assertEqual(401, response.status_code)

    def test_post_fails_with_unauthorized_if_no_token_sent(self):
        response = requests.post(self.url, data = '{}')
        self.assertEqual(401, response.status_code)

    def test_put_fails_with_unauthorized_if_no_token_sent(self):
        response = requests.put(self.url + '/1234', data = '{}')
        self.assertEqual(401, response.status_code)

    def test_delete_fails_with_unauthorized_if_no_token_sent(self):
        response = requests.delete(self.url + '/1234')
        self.assertEqual(401, response.status_code)

    def test_get_fails_for_non_link(self):
        response = requests.get(self.url + '/no-such-id', headers = jwt())
        self.assertEqual(404, response.status_code)

    def test_delete_fails_for_non_link(self):
        response = requests.delete(self.url + '/no-such-id', headers = jwt())
        self.assertEqual(404, response.status_code)

    def test_post_fails_for_non_json(self):
        response = requests.post(self.url, data = 'not json', headers = jwt())
        self.assertEqual(400, response.status_code)
        self.assertIn('The data is not a JSON string', response.text)

    def test_post_fails_with_id(self):
        response = requests.post(self.url, data = '{"id": "fake-id"}', headers = jwt())
        self.assertEqual(400, response.status_code)
        self.assertIn('id cannot be set externally', response.text)

    def test_post_fails_with_created_at(self):
        response = requests.post(self.url, data = '{"created_at": "noon"}', headers = jwt())
        self.assertEqual(400, response.status_code)
        self.assertIn('created_at cannot be set externally', response.text)

    def test_post_fails_with_created_by(self):
        response = requests.post(self.url, data = '{"created_by": "me"}', headers = jwt())
        self.assertEqual(400, response.status_code)
        self.assertIn('created_by cannot be set externally', response.text)

    def test_post_fails_for_empty_json(self):
        response = requests.post(self.url, data = '{}', headers = jwt())
        self.assertEqual(400, response.status_code)
        self.assertIn('source and target must be set', response.text)

    def test_post_fails_for_invalid_source(self):
        response = requests.post(self.url, headers = jwt(), data = '''
        {{
            "source": "nonsense",
            "target": "{0}"
        }}
        '''.format(self.item_1_id))

        self.assertEqual(400, response.status_code)
        self.assertIn('source must be a valid item id', response.text)

    def test_post_fails_for_invalid_target(self):
        response = requests.post(self.url, headers = jwt(), data = '''
        {{
            "source": "{0}",
            "target": "nonsense"
        }}
        '''.format(self.item_1_id))

        self.assertEqual(400, response.status_code)
        self.assertIn('target must be a valid item id', response.text)

    def test_post_fails_for_source_same_as_target(self):
        response = requests.post(self.url, headers = jwt(), data = '''
        {{
            "source": "{0}",
            "target": "{0}"
        }}
        '''.format(self.item_1_id))

        self.assertEqual(400, response.status_code)
        self.assertIn('source and target must be different', response.text)

    def test_post_succeeds_for_valid_source_and_target(self):
        response = requests.post(self.url, headers = jwt(), data = '''
        {{
            "source": "{0}",
            "target": "{1}"
        }}
        '''.format(self.item_1_id, self.item_2_id))

        self.assertEqual(200, response.status_code)

    def test_get_succeeds_for_new_link(self):
        post_response = requests.post(self.url, headers = jwt(), data = '''
        {{
            "properties": {{
                "type": "IMPLEMENTS"
            }},
            "source": "{0}",
            "target": "{1}"
        }}
        '''.format(self.item_1_id, self.item_2_id))
        self.assertEqual(200, post_response.status_code)

        new_link = post_response.json()

        get_response = requests.get(self.url + '/' + new_link['id'], headers = jwt())
        self.assertEqual(200, get_response.status_code)

        got_link = get_response.json()

        self.assertDictEqual(new_link, got_link)

    def test_delete_succeeds_for_new_link(self):
        post_response = requests.post(self.url, headers = jwt(), data = '''
        {{
            "properties": {{
                "type": "IMPLEMENTS"
            }},
            "source": "{0}",
            "target": "{1}"
        }}
        '''.format(self.item_1_id, self.item_2_id))
        self.assertEqual(200, post_response.status_code)

        new_link = post_response.json()

        delete_response = requests.delete(self.url + '/' + new_link['id'], headers = jwt())
        self.assertEqual(200, delete_response.status_code)

        deleted_link = delete_response.json()

        self.assertDictEqual(new_link, deleted_link)

        get_response = requests.get(self.url + '/' + new_link['id'], headers = jwt())
        self.assertEqual(404, get_response.status_code)

    def test_post_ignores_extra_fields(self):
        response = requests.post(self.url, headers = jwt(), data = '''
        {{
            "properties": {{
                "type": "IMPLEMENTS"
            }},
            "secret": "shhhhhhhhhhh",
            "source": "{0}",
            "target": "{1}"
        }}
        '''.format(self.item_1_id, self.item_2_id))

        self.assertEqual(200, response.status_code)

        json = response.json()
        self.assertIn('id', json)
        self.assertIn('created_at', json)
        self.assertIn('created_by', json)
        self.assertIn('properties', json)
        self.assertIn('source', json)
        self.assertIn('target', json)

        self.assertNotIn('secret', json)

    def test_put_fails_for_no_id(self):
        response = requests.put(self.url, headers = jwt())
        self.assertEqual(404, response.status_code)

    def test_put_fails_for_non_json(self):
        response = requests.put(self.url + '/1234', data = 'not json', headers = jwt())
        self.assertEqual(400, response.status_code)
        self.assertIn('The data is not a JSON string', response.text)

    def test_put_fails_for_non_existent_link(self):
        response = requests.put(self.url + '/1234', data = '{}', headers = jwt())
        self.assertEqual(404, response.status_code)

    def test_put_can_change_properties(self):
        put_json = deepcopy(self.link)
        put_json['properties']['type'] = 'RELATES TO'

        put_response = requests.put(self.url + '/' + put_json['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(200, put_response.status_code)

        get_response = requests.get(self.url + '/' + put_json['id'], headers = jwt())
        self.assertEqual(200, get_response.status_code)

        got_json = get_response.json()

        self.assertDictEqual(put_json, got_json)

    def test_put_fails_if_empty_link_sent(self):
        response = requests.put(self.url + '/' + self.link['id'], data = '{}', headers = jwt())
        self.assertEqual(400, response.status_code)
        self.assertIn('id cannot be modified', response.text)

    def test_put_fails_if_id_modified(self):
        put_json = deepcopy(self.link)
        put_json['id'] = '1234'

        put_response = requests.put(self.url + '/' + self.link['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(400, put_response.status_code)
        self.assertIn('id cannot be modified', put_response.text)

    def test_put_fails_if_created_at_modified(self):
        put_json = deepcopy(self.link)
        put_json['created_at'] = 'yesterday'

        put_response = requests.put(self.url + '/' + self.link['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(400, put_response.status_code)
        self.assertIn('created_at cannot be modified', put_response.text)

    def test_put_fails_if_created_by_modified(self):
        put_json = deepcopy(self.link)
        put_json['created_by'] = 'magic'

        put_response = requests.put(self.url + '/' + self.link['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(400, put_response.status_code)
        self.assertIn('created_by cannot be modified', put_response.text)

    def test_put_fails_if_source_invalid(self):
        put_json = deepcopy(self.link)
        put_json['source'] = 'rubbish'

        put_response = requests.put(self.url + '/' + self.link['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(400, put_response.status_code)
        self.assertIn('source must be a valid item id', put_response.text)

    def test_put_fails_if_target_invalid(self):
        put_json = deepcopy(self.link)
        put_json['target'] = 'rubbish'

        put_response = requests.put(self.url + '/' + self.link['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(400, put_response.status_code)
        self.assertIn('target must be a valid item id', put_response.text)

    def test_put_fails_if_source_same_as_target(self):
        put_json = deepcopy(self.link)
        put_json['target'] = put_json['source']

        put_response = requests.put(self.url + '/' + self.link['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(400, put_response.status_code)
        self.assertIn('source and target must be different', put_response.text)

    def test_put_ignores_extra_fields(self):
        put_json = deepcopy(self.link)
        put_json['secret'] = 'tell no-one'

        put_response = requests.put(self.url + '/' + self.link['id'], data = dumps(put_json), headers = jwt())
        self.assertEqual(200, put_response.status_code)
        self.assertNotIn('secret', put_response.json())

import requests
import unittest

from copy import deepcopy
from json import dumps

def jwt():
    return {'Authorization': 'Bearer abcd'}

class TestBlackBoxSearchAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # item_1 is a PROJECT that CONTAINS an EPIC item_2 and
        # item_3 is a STORY that IMPLEMENTS part of item_2.

        cls.url_items = 'http://localhost:2207/v1/items'
        cls.item_1 = requests.post(cls.url_items, headers = jwt(), data = '''
        {
            "properties": {
                "type": "PROJECT"
            }
        }''').json()
        cls.item_2 = requests.post(cls.url_items, headers = jwt(), data = '''
        {
            "properties": {
                "type": "EPIC"
            }
        }''').json()
        cls.item_3 = requests.post(cls.url_items, headers = jwt(), data = '''
        {
            "properties": {
                "type": "STORY"
            }
        }''').json()

        cls.url_links = 'http://localhost:2207/v1/links'
        cls.link_12 = requests.post(cls.url_links, headers = jwt(), data = '''
        {{
            "properties": {{
                "type": "CONTAINS"
            }},
            "source": "{0}",
            "target": "{1}"
        }}
        '''.format(cls.item_1['id'], cls.item_2['id'])).json()
        cls.link_32 = requests.post(cls.url_links, headers = jwt(), data = '''
        {{
            "properties": {{
                "type": "IMPLEMENTS"
            }},
            "source": "{0}",
            "target": "{1}"
        }}
        '''.format(cls.item_3['id'], cls.item_2['id'])).json()

    def test_search_item_fails_with_unauthorized_if_no_token_sent(self):
        response = requests.get(self.url_items + '?type=PROJECT')
        self.assertEqual(401, response.status_code)

    def test_search_item_gets_empty_list_if_no_matches(self):
        response = requests.get(self.url_items + '?type=MYSTERY', headers = jwt())
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json())

    def test_search_item_succeeds_if_items_match(self):
        response = requests.get(self.url_items + '?type=PROJECT', headers = jwt())
        self.assertEqual(200, response.status_code)
        item_list = response.json()
        self.assertTrue(self.item_1 in item_list)
        self.assertFalse(self.item_2 in item_list)
        self.assertFalse(self.item_3 in item_list)

    def test_search_link_fails_with_unauthorized_if_no_token_sent(self):
        response = requests.get(self.url_links + '?source=1234')
        self.assertEqual(401, response.status_code)

    def test_search_link_gets_empty_list_if_no_matches(self):
        response = requests.get(self.url_links + '?source=MYSTERY', headers = jwt())
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json())

    def test_search_link_by_source(self):
        response = requests.get(self.url_links + '?source=' + self.item_1['id'], headers = jwt())
        self.assertEqual(200, response.status_code)
        link_list = response.json()
        self.assertTrue(self.link_12 in link_list)
        self.assertFalse(self.link_32 in link_list)

    def test_search_link_by_target(self):
        response = requests.get(self.url_links + '?target=' + self.item_2['id'], headers = jwt())
        self.assertEqual(200, response.status_code)
        link_list = response.json()
        self.assertTrue(self.link_12 in link_list)
        self.assertTrue(self.link_32 in link_list)

    def test_search_link_by_either(self):
        response = requests.get(self.url_links + '?either=' + self.item_3['id'], headers = jwt())
        self.assertEqual(200, response.status_code)
        link_list = response.json()
        self.assertFalse(self.link_12 in link_list)
        self.assertTrue(self.link_32 in link_list)

from thelca.error import NotAuthorisedError, NotSavedError, ItemNotFound
from thelca.model import Item
from thelca.api import API

import copy
import unittest

import logging
logging.basicConfig(level=999)

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.api = API('1.0')
        self.token = 'ABCD'

    def test_get_item_exception_with_no_token(self):
        item = self.api.create_item({}, self.token)
        self.assertRaises(NotAuthorisedError,
                          self.api.get_item, item.id, None)

    def test_get_item_exception_if_non_existent(self):
        self.assertRaises(ItemNotFound,
                          self.api.get_item, '1234', self.token)

    def test_create_item_exception_with_no_token(self):
        self.assertRaises(NotAuthorisedError,
                          self.api.create_item, {}, None)

    def test_create_item_exception_if_id_exists(self):
        self.assertRaises(NotSavedError,
                          self.api.create_item, {'id': 0}, self.token)

    def test_create_item_and_recover_it(self):
        dictionary = {'properties': {'type': 'BUG'}}

        new_item = self.api.create_item(dictionary, self.token)

        self.assertFalse(new_item.id is None)
        self.assertFalse(new_item.created_at is None)
        self.assertEqual('a-test-only-id-ABCD', new_item.created_by)
        self.assertEqual('BUG', new_item.properties['type'])

        same_item = self.api.get_item(new_item.id, self.token)

        self.assertEqual(new_item.created_at, same_item.created_at)
        self.assertEqual('a-test-only-id-ABCD', same_item.created_by)
        self.assertEqual('BUG', same_item.properties['type'])

    def test_create_item_and_update_it(self):
        dictionary = {'properties': {'type': 'EPIC'}}

        item = self.api.create_item(dictionary, self.token)

        update = copy.deepcopy(item)
        update.properties['status'] = 'DONE'

        new_item = self.api.update_item(item.id, update, self.token)

        self.assertEqual('EPIC', new_item.properties['type'])
        self.assertEqual('DONE', new_item.properties['status'])

    def test_update_item_exception_with_no_token(self):
        item = self.api.create_item({}, self.token)
        self.assertRaises(NotAuthorisedError,
                          self.api.update_item, item.id, Item(), None)

    def test_update_item_exception_if_non_existent(self):
        self.assertRaises(ItemNotFound,
                          self.api.update_item, '1234', Item(), self.token)

    def test_update_item_exception_if_id_modified(self):
        item = self.api.create_item({}, self.token)

        update = copy.deepcopy(item)
        update.id = 'fake-id'

        self.assertRaises(NotSavedError,
                          self.api.update_item, item.id, update, self.token)

    def test_update_item_exception_if_created_at_modified(self):
        item = self.api.create_item({}, self.token)

        update = copy.deepcopy(item)
        update.created_at = 'yesterday'

        self.assertRaises(NotSavedError,
                          self.api.update_item, item.id, update, self.token)

    def test_update_item_exception_if_created_by_modified(self):
        item = self.api.create_item({}, self.token)

        update = copy.deepcopy(item)
        update.created_by = 'Mr Bean'

        self.assertRaises(NotSavedError,
                          self.api.update_item, item.id, update, self.token)

if __name__ == '__main__':
    unittest.main()

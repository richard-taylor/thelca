from thelca.error import NotAuthorisedError, NotSavedError, ItemNotFound
from thelca.model import Item
from thelca.api import API

import unittest

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.api = API('1.0')
        self.user = self.api.default_user()

    def test_get_item_exception_with_no_user(self):
        self.assertRaises(NotAuthorisedError,
                          self.api.get_item, '1234', None)

    def test_get_item_exception_if_non_existent(self):
        self.assertRaises(ItemNotFound,
                          self.api.get_item, '1234', self.user)

    def test_create_item_exception_with_no_user(self):
        self.assertRaises(NotAuthorisedError,
                          self.api.create_item, Item(), None)

    def test_create_item_exception_if_id_exists(self):
        self.assertRaises(NotSavedError,
                          self.api.create_item, Item(self.user), self.user)

    def test_create_item_and_recover_it(self):
        empty_item = Item()
        empty_item.properties = {"type": "BUG"}

        new_item = self.api.create_item(empty_item, self.user)

        self.assertFalse(new_item.id is None)
        self.assertFalse(new_item.created_at is None)
        self.assertEqual(self.user.id, new_item.created_by)
        self.assertEqual('BUG', new_item.properties['type'])

        same_item = self.api.get_item(new_item.id, self.user)

        self.assertEqual(new_item.created_at, same_item.created_at)
        self.assertEqual(self.user.id, same_item.created_by)
        self.assertEqual('BUG', same_item.properties['type'])

if __name__ == '__main__':
    unittest.main()

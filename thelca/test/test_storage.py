from copy import deepcopy
from thelca.error import ItemNotFound
from thelca.model import Item
from thelca.storage import MemoryStore

import unittest

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.store = MemoryStore()
        self.user = '1-2-3-4'

    def test_save_item_and_find_item(self):
        item1 = Item(self.user, {'properties': {"type": "ABC"}})
        item2 = Item(self.user, {'properties': {"type": "123"}})

        self.store.save_item(item1)
        self.store.save_item(item2)

        found1 = self.store.find_item(item1.id)
        found2 = self.store.find_item(item2.id)

        self.assertTrue(isinstance(found1, Item))
        self.assertEqual(item1.id, found1.id)
        self.assertEqual('ABC', found1.properties['type'])

        self.assertTrue(isinstance(found2, Item))
        self.assertEqual(item2.id, found2.id)
        self.assertEqual('123', found2.properties['type'])

    def test_modify_item(self):
        original_item = Item(self.user, {'properties': {"type": "ABC"}})

        self.store.save_item(original_item)

        new_item = deepcopy(original_item)
        new_item.properties['type'] = 'DEF'

        self.store.modify_item(new_item)

        changed = self.store.find_item(original_item.id)

        self.assertTrue(isinstance(changed, Item))
        self.assertEqual('DEF', changed.properties['type'])

    def test_find_non_existent_item(self):
        item1 = Item(self.user, {'properties': {"type": "ABC"}})
        item2 = Item(self.user, {'properties': {"type": "123"}})

        self.store.save_item(item1)
        self.store.save_item(item2)

        self.assertRaises(ItemNotFound, self.store.find_item, 'not-an-id')

if __name__ == '__main__':
    unittest.main()

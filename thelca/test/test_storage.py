from thelca.model import Item, User
from thelca.storage import MemoryStore, ItemNotFound
import unittest

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.root = User()
        self.store = MemoryStore()

    def test_save_item_and_find_item(self):
        item1 = Item(self.root, {"type": "ABC"})
        item2 = Item(self.root, {"type": "123"})

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

    def test_find_non_existent_item(self):
        item1 = Item(self.root, {"type": "ABC"})
        item2 = Item(self.root, {"type": "123"})

        self.store.save_item(item1)
        self.store.save_item(item2)

        self.assertRaises(ItemNotFound, self.store.find_item, 'not-an-id')

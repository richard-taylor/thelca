from thelca.model import Item, Link
import unittest

class TestModel(unittest.TestCase):

    def setUp(self):
        self.user = 'dummy-user-id'

    def test_empty_item(self):
        item = Item()

        self.assertTrue(item.id is None)
        self.assertTrue(item.created_at is None)
        self.assertTrue(item.created_by is None)
        self.assertTrue(item.properties is None)

    def test_create_item(self):
        item = Item(self.user, {'TYPE': 'EPIC', 'DESCRIPTION': 'big'})

        self.assertFalse(item.id is None)
        self.assertFalse(item.created_at is None)
        self.assertEqual(self.user, item.created_by)
        self.assertEqual('EPIC', item.properties['TYPE'])
        self.assertEqual('big', item.properties['DESCRIPTION'])

    def test_empty_link(self):
        link = Link()

        self.assertTrue(link.id is None)
        self.assertTrue(link.created_at is None)
        self.assertTrue(link.created_by is None)
        self.assertTrue(link.source is None)
        self.assertTrue(link.target is None)
        self.assertTrue(link.properties is None)

    def test_create_link(self):
        item1 = Item(self.user)
        item2 = Item(self.user)

        link = Link(self.user, item1.id, item2.id, {'TYPE': 'EXPLAINS'})

        self.assertFalse(link.id is None)
        self.assertFalse(link.created_at is None)
        self.assertEqual(self.user, link.created_by)
        self.assertEqual(item1.id, link.source)
        self.assertEqual(item2.id, link.target)
        self.assertEqual('EXPLAINS', link.properties['TYPE'])

if __name__ == '__main__':
    unittest.main()

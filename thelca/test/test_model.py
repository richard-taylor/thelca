from thelca.model import Item, Link, User
import unittest

class TestModel(unittest.TestCase):

    def setUp(self):
        self.root = User()
        self.user = User(self.root)

    def test_empty_item(self):
        item = Item();

        self.assertTrue(item.id is None)
        self.assertTrue(item.created_at is None)
        self.assertTrue(item.created_by is None)
        self.assertTrue(item.properties is None)

    def test_create_item(self):
        item = Item(self.user, {'TYPE': 'EPIC', 'DESCRIPTION': 'big'});

        self.assertFalse(item.id is None)
        self.assertFalse(item.created_at is None)
        self.assertEqual(self.user.id, item.created_by)
        self.assertEqual('EPIC', item.properties['TYPE'])
        self.assertEqual('big', item.properties['DESCRIPTION'])

    def test_empty_link(self):
        link = Link();

        self.assertTrue(link.id is None)
        self.assertTrue(link.created_at is None)
        self.assertTrue(link.created_by is None)
        self.assertTrue(link.src is None)
        self.assertTrue(link.dest is None)
        self.assertTrue(link.properties is None)

    def test_create_link(self):
        item1 = Item(self.user)
        item2 = Item(self.user)

        link = Link(self.user, item1, item2, {'TYPE': 'EXPLAINS'});

        self.assertFalse(link.id is None)
        self.assertFalse(link.created_at is None)
        self.assertEqual(self.user.id, link.created_by)
        self.assertEqual(item1.id, link.src)
        self.assertEqual(item2.id, link.dest)
        self.assertEqual('EXPLAINS', link.properties['TYPE'])

    def test_create_root_user(self):
        root_user = User();

        self.assertEqual('root', root_user.id)
        self.assertTrue(root_user.created_at is None)
        self.assertTrue(root_user.created_by is None)

    def test_create_normal_user(self):
        normal_user = User(self.root);

        self.assertFalse(normal_user.id is None)
        self.assertFalse(normal_user.created_at is None)
        self.assertEqual(self.root.id, normal_user.created_by)

if __name__ == '__main__':
    unittest.main()

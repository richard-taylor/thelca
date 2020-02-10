from thelca.model import Item, User
from thelca.translator import JSON, TranslationError
import unittest

class TestTranslator(unittest.TestCase):

    def setUp(self):
        self.root = User()
        self.user = User(self.root)
        self.translate = JSON()

    def test_empty_item_to_json(self):
        item = Item()
        json = self.translate.from_item(item)

        self.assertEqual('{"created_at": null, "created_by": null, "id": null, "properties": null}', json)

    def test_item_to_json(self):
        item = Item(self.root, {'type': 'STORY'})
        json = self.translate.from_item(item)

        self.assertTrue('"created_at": "' in json)
        self.assertTrue('"created_by": "root"' in json)
        self.assertTrue('"id": "' in json)
        self.assertTrue('"properties": {"type": "STORY"}' in json)

    def test_invalid_json_to_item(self):
        self.assertRaises(TranslationError, self.translate.to_item, '')
        self.assertRaises(TranslationError, self.translate.to_item, '{')
        self.assertRaises(TranslationError, self.translate.to_item, '{blah}')
        self.assertRaises(TranslationError, self.translate.to_item, '}')

    def test_json_to_item(self):
        json = '{"id": "1234", "properties": {"type": "EPIC"}}'
        item = self.translate.to_item(json)

        self.assertTrue(isinstance(item, Item))
        self.assertEqual("1234", item.id)
        self.assertEqual("EPIC", item.properties['type'])

from thelca.model import Item
from thelca.translator import JSON, TranslationError

import unittest

class TestTranslator(unittest.TestCase):

    def setUp(self):
        self.translate = JSON()
        self.user = 'the-user-id'

    def test_valid_json_to_dict(self):
        dict = self.translate.to_dictionary('{"a": "b"}')
        self.assertDictEqual({'a': 'b'}, dict)

    def test_invalid_json_to_dict(self):
        self.assertRaises(TranslationError,
                          self.translate.to_dictionary, 'not json')

    def test_empty_item_to_json(self):
        item = Item()
        json = self.translate.from_item(item)

        self.assertEqual('{"created_at": null, "created_by": null, "id": null, "properties": null}', json)

    def test_item_to_json(self):
        item = Item(self.user, {'type': 'STORY'})
        json = self.translate.from_item(item)

        self.assertTrue('"created_at": "' in json)
        self.assertTrue('"created_by": "the-user-id"' in json)
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

    def test_json_to_item_ignores_extra_fields(self):
        json = '{"id": "1234", "bogus": "rubbish"}'
        item = self.translate.to_item(json)

        self.assertTrue(isinstance(item, Item))
        self.assertEqual("1234", item.id)
        self.assertNotIn("bogus", item.__dict__)

if __name__ == '__main__':
    unittest.main()

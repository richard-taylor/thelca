from thelca.error import ItemNotFound, LinkNotFound

import thelca.api
import thelca.restore

import unittest

class TestRestore(unittest.TestCase):

    def setUp(self):
        self.item_ids = [
            "4bd8cb57-1001-4318-b2f6-bc9b6cf10c3a",
            "25cbe3f6-e5db-4dc9-92ae-a81868b345ae"]

    def test_restore_from_event_log(self):
        for id in self.item_ids:
            self.assertRaises(ItemNotFound, thelca.api.storage.find_item, id)

        thelca.restore.from_event_log('data/event-log')

        item = thelca.api.storage.find_item("4bd8cb57-1001-4318-b2f6-bc9b6cf10c3a")
        self.assertEqual("a-test-only-id-abcd", item.created_by)
        self.assertDictEqual({"status": "OPEN", "type": "BUG"}, item.properties)

        item = thelca.api.storage.find_item("25cbe3f6-e5db-4dc9-92ae-a81868b345ae")
        self.assertEqual("a-test-only-id-abcd", item.created_by)
        self.assertDictEqual({"type": "STORY"}, item.properties)

        link = thelca.api.storage.find_link("0b25d518-0b10-462e-a936-859ec29fd4cc")
        self.assertEqual("a-test-only-id-abcd", link.created_by)
        self.assertEqual("bd671302-50a4-496d-94ac-1851f1571a80", link.source)
        self.assertEqual("daf625aa-fc27-4f42-819a-c4a293af0018", link.target)
        self.assertDictEqual({"type": "BLOCKS"}, link.properties)

        self.assertRaises(LinkNotFound,
            thelca.api.storage.find_link,
            "d248a21f-756d-4413-b306-4f8a5835f6bb") # it was deleted

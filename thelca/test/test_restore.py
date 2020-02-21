from thelca.error import ItemNotFound
from thelca.model import Item

import thelca.api
import thelca.restore

import unittest

class TestRestore(unittest.TestCase):

    def setUp(self):
        self.all_ids = [
            "c045bdf2-66af-4d3c-a10e-1858fb5ec8ee",
            "3621b06f-c910-4212-9d6d-a5255324e298",
            "998a8145-fedb-4416-9350-4f59f22756b1",
            "60468769-29dd-422a-86d3-cdf382eadceb",
            "1a47f636-01a8-47d2-a20a-6761d66b5ff0",
            "b9555837-59f2-4fb1-bbde-d1a819f1b280",
            "132d9851-29cf-4f4c-89fe-22ab11665852",
            "114aec65-8e47-4a8d-a663-7695d664a6a1",
            "97f16591-fe05-44ce-b805-52e99012f945"]

    def test_restore_from_event_log(self):
        for id in self.all_ids:
            self.assertRaises(ItemNotFound, thelca.api.storage.find_item, id)

        thelca.restore.from_event_log('data/event-log')

        for id in self.all_ids:
            item = thelca.api.storage.find_item(id)
            self.assertEqual("a-test-only-id-abcd", item.created_by)

        item = thelca.api.storage.find_item("c045bdf2-66af-4d3c-a10e-1858fb5ec8ee")
        self.assertDictEqual({"a": "b"}, item.properties)

        item = thelca.api.storage.find_item("3621b06f-c910-4212-9d6d-a5255324e298")
        self.assertDictEqual({"status": "OPEN", "type": "BUG"}, item.properties)

        item = thelca.api.storage.find_item("998a8145-fedb-4416-9350-4f59f22756b1")
        self.assertIsNone(item.properties)

        item = thelca.api.storage.find_item("60468769-29dd-422a-86d3-cdf382eadceb")
        self.assertDictEqual({"type": "STORY"}, item.properties)

        item = thelca.api.storage.find_item("1a47f636-01a8-47d2-a20a-6761d66b5ff0")
        self.assertIsNone(item.properties)

        item = thelca.api.storage.find_item("b9555837-59f2-4fb1-bbde-d1a819f1b280")
        self.assertIsNone(item.properties)

        item = thelca.api.storage.find_item("132d9851-29cf-4f4c-89fe-22ab11665852")
        self.assertIsNone(item.properties)

        item = thelca.api.storage.find_item("114aec65-8e47-4a8d-a663-7695d664a6a1")
        self.assertIsNone(item.properties)

        item = thelca.api.storage.find_item("97f16591-fe05-44ce-b805-52e99012f945")
        self.assertDictEqual({"type": "STORY"}, item.properties)

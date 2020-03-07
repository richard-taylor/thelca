import json

from thelca.model import Item, Link

class TranslationError(Exception):
    pass

class NotJsonError(TranslationError):
    def __init__(self):
        super().__init__("The data is not a JSON string")

class JSON:

    def to_dictionary(self, string):
        try:
            return json.loads(string)
        except json.JSONDecodeError:
            raise NotJsonError()

    def from_item(self, item):
        return json.dumps(vars(item), sort_keys=True)

    def from_item_list(self, item_list):
        return json.dumps([vars(item) for item in item_list], sort_keys=True)

    def to_item(self, string):
        try:
            return Item.from_dictionary(json.loads(string))
        except json.JSONDecodeError:
            raise NotJsonError()

    def from_link(self, link):
        return json.dumps(vars(link), sort_keys=True)

    def from_link_list(self, link_list):
        return json.dumps([vars(link) for link in link_list], sort_keys=True)

    def to_link(self, string):
        try:
            return Link.from_dictionary(json.loads(string))
        except json.JSONDecodeError:
            raise NotJsonError()

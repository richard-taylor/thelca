import json

from thelca.model import Item

class TranslationError(Exception):
    pass

class JSON:

    def from_item(self, item):
        return json.dumps(vars(item))

    def to_item(self, string):
        item = Item()
        try:
            item.__dict__.update(json.loads(string))
            return item
        except json.JSONDecodeError:
            raise TranslationError("The data is not a JSON string")

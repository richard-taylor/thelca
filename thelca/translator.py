import json

from thelca.model import Item

class TranslationError(Exception):
    pass

class JSON:

    def to_dictionary(self, string):
        try:
            return json.loads(string)
        except json.JSONDecodeError:
            raise TranslationError("The data is not a JSON string")

    def from_item(self, item):
        return json.dumps(vars(item), sort_keys=True)

    def to_item(self, string):
        item = Item()
        try:
            dictionary = json.loads(string)
            for key in vars(item):
                if key in dictionary:
                    item.__dict__[key] = dictionary[key]
            return item
        except json.JSONDecodeError:
            raise TranslationError("The data is not a JSON string")

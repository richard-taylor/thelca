import json

from thelca.model import Item, Link

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
        return self.fill_object(string, Item())

    def from_link(self, link):
        return json.dumps(vars(link), sort_keys=True)

    def to_link(self, string):
        return self.fill_object(string, Link())

    def fill_object(self, string, object):
        try:
            dictionary = json.loads(string)
            for key in vars(object):
                if key in dictionary:
                    object.__dict__[key] = dictionary[key]
            return object
        except json.JSONDecodeError:
            raise TranslationError("The data is not a JSON string")

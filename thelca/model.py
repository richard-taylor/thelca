import uuid
from thelca.time import current_time_UTC

class Trackable:
    def __init__(self, created_by):
        if created_by is None:
            self.id = None
            self.created_by = None
            self.created_at = None
        else:
            self.id = str(uuid.uuid4())
            self.created_by = created_by
            self.created_at = current_time_UTC()

    @classmethod
    def from_dictionary(cls, dictionary):
        object = cls()
        for key in vars(object):
            if key in dictionary:
                object.__dict__[key] = dictionary[key]
        return object

    def check_immutables(self, dictionary):
        if 'id' in dictionary:
            raise ValueError("id cannot be set externally")

        if 'created_at' in dictionary:
            raise ValueError("created_at cannot be set externally")

        if 'created_by' in dictionary:
            raise ValueError("created_by cannot be set externally")

    def check_update(self, proposed):
        if self.id != proposed.id:
            raise ValueError("id cannot be modified")

        if self.created_at != proposed.created_at:
            raise ValueError("created_at cannot be modified")

        if self.created_by != proposed.created_by:
            raise ValueError("created_by cannot be modified")

class Item(Trackable):
    def __init__(self, created_by = None, dictionary = None):
        super().__init__(created_by)
        if dictionary is None:
            self.properties = {}
        else:
            self.check_immutables(dictionary)
            self.properties = dictionary.get('properties', {})

class Link(Trackable):
    def __init__(self, created_by = None, dictionary = None):
        super().__init__(created_by)
        if dictionary is None:
            self.source = None
            self.target = None
            self.properties = {}
        else:
            self.check_immutables(dictionary)
            self.source = dictionary.get('source')
            self.target = dictionary.get('target')
            self.properties = dictionary.get('properties', {})

    def check_endpoints(self, storage):
        if self.source is None or self.target is None:
            raise ValueError("source and target must be set")

        if self.source == self.target:
            raise ValueError("source and target must be different")

        if not storage.has_item(self.source):
            raise ValueError("source must be a valid item id")

        if not storage.has_item(self.target):
            raise ValueError("target must be a valid item id")

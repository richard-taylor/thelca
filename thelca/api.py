import json

from thelca.error import NotAuthorisedError, NotSavedError
from thelca.model import Item, User
from thelca.storage import MemoryStore

storage = MemoryStore()

class API:
    def __init__(self, version):
        self.version = version
        self.root = User()
        self.user = User(self.root)
        self.user.name = 'Reginald Dustbin'

    def default_user(self):
        return self.user

    def get_item(self, id, requesting_user):
        if requesting_user is None:
            raise NotAuthorisedError()

        return storage.find_item(id)

    def create_item(self, dictionary, requesting_user):
        if requesting_user is None:
            raise NotAuthorisedError()

        if 'id' in dictionary:
            raise NotSavedError("id cannot be set externally")

        if 'created_at' in dictionary:
            raise NotSavedError("created_at cannot be set externally")

        if 'created_by' in dictionary:
            raise NotSavedError("created_by cannot be set externally")

        if 'properties' in dictionary:
            item = Item(requesting_user, dictionary['properties'])
        else:
            item = Item(requesting_user)

        storage.save_item(item)
        return item

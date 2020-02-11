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

    def create_item(self, item, requesting_user):
        if requesting_user is None:
            raise NotAuthorisedError()

        if item.id is not None:
            raise NotSavedError("The Item already has an ID")
        else:
            item.mark_creation(requesting_user)

        storage.save_item(item)
        return item

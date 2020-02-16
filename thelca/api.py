import json

from thelca.auth import Authority
from thelca.error import NotSavedError
from thelca.model import Item
from thelca.logging import EventLogger
from thelca.storage import MemoryStore

authority = Authority()
logging = EventLogger()
storage = MemoryStore()

class API:
    def __init__(self, version):
        self.version = version

    def get_item(self, id, token):
        item = storage.find_item(id)
        user = authority.check_read_item(token, item)

        logging.item_read(item, user)
        return item

    def create_item(self, dictionary, token):
        user = authority.check_create_item(token, dictionary)

        if 'id' in dictionary:
            raise NotSavedError("id cannot be set externally")

        if 'created_at' in dictionary:
            raise NotSavedError("created_at cannot be set externally")

        if 'created_by' in dictionary:
            raise NotSavedError("created_by cannot be set externally")

        if 'properties' in dictionary:
            item = Item(user, dictionary['properties'])
        else:
            item = Item(user)

        storage.save_item(item)
        logging.item_created(item, user)
        return item

    def update_item(self, id, item, token):
        current = storage.find_item(id)
        user = authority.check_update_item(token, current, item)

        if current.id != item.id:
            raise NotSavedError("id cannot be modified")

        if current.created_at != item.created_at:
            raise NotSavedError("created_at cannot be modified")

        if current.created_by != item.created_by:
            raise NotSavedError("created_by cannot be modified")

        storage.save_item(item)
        logging.item_updated(item, user)
        return item

import json

from thelca.auth import Authority
from thelca.error import NotSavedError
from thelca.model import Item, Link
from thelca.logging import EventLogger
from thelca.storage import MemoryStore

authority = Authority()
logging = EventLogger()
storage = MemoryStore()

class API:
    def __init__(self, version):
        self.version = version

    def read_item(self, id, token):
        item = storage.find_item(id)
        user = authority.check_read_item(token, item)

        logging.item_read(item, user)
        return item

    def create_item(self, dictionary, token):
        user = authority.check_create_item(token, dictionary)
        try:
            item = Item(user, dictionary)

        except ValueError as error:
            raise NotSavedError(error)

        storage.save_item(item)
        logging.item_created(item, user)
        return item

    def update_item(self, id, item, token):
        current = storage.find_item(id)
        user = authority.check_update_item(token, current, item)
        try:
            current.check_update(item)

        except ValueError as error:
            raise NotSavedError(error)

        storage.modify_item(item)
        logging.item_updated(current, item, user)
        return item

    def read_link(self, id, token):
        link = storage.find_link(id)
        user = authority.check_read_link(token, link)

        logging.link_read(link, user)
        return link

    def create_link(self, dictionary, token):
        user = authority.check_create_link(token, dictionary)
        try:
            link = Link(user, dictionary)
            link.check_endpoints(storage)

        except ValueError as error:
            raise NotSavedError(error)

        storage.save_link(link)
        logging.link_created(link, user)
        return link

    def update_link(self, id, link, token):
        current = storage.find_link(id)
        user = authority.check_update_link(token, current, link)
        try:
            current.check_update(link)
            link.check_endpoints(storage)

        except ValueError as error:
            raise NotSavedError(error)

        storage.modify_link(link)
        logging.link_updated(current, link, user)
        return link

    def delete_link(self, id, token):
        link = storage.find_link(id)
        user = authority.check_delete_link(token, link)

        storage.remove_link(id)
        logging.link_deleted(link, user)
        return link

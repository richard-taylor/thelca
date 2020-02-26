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

        self._no_immutables(dictionary)

        item = Item(user, dictionary.get('properties'))

        storage.save_item(item)
        logging.item_created(item, user)
        return item

    def update_item(self, id, item, token):
        current = storage.find_item(id)
        user = authority.check_update_item(token, current, item)

        self._fixed_immutables(current, item)

        storage.modify_item(current, item)
        logging.item_updated(current, item, user)
        return item

    def read_link(self, id, token):
        link = storage.find_link(id)
        user = authority.check_read_link(token, link)

        logging.link_read(link, user)
        return link

    def create_link(self, dictionary, token):
        user = authority.check_create_link(token, dictionary)

        self._no_immutables(dictionary)

        link = Link(user,
                    dictionary.get('source'),
                    dictionary.get('target'),
                    dictionary.get('properties'))

        self._source_and_target_valid(link)

        storage.save_link(link)
        logging.link_created(link, user)
        return link

    def update_link(self, id, link, token):
        current = storage.find_link(id)
        user = authority.check_update_link(token, current, link)

        self._fixed_immutables(current, link)
        self._source_and_target_valid(link)

        storage.modify_link(current, link)
        logging.link_updated(current, link, user)
        return link

    def delete_link(self, id, token):
        link = storage.find_link(id)
        user = authority.check_delete_link(token, link)

        storage.remove_link(link)
        logging.link_deleted(link, user)
        return link

    def _no_immutables(self, dictionary):
        if 'id' in dictionary:
            raise NotSavedError("id cannot be set externally")

        if 'created_at' in dictionary:
            raise NotSavedError("created_at cannot be set externally")

        if 'created_by' in dictionary:
            raise NotSavedError("created_by cannot be set externally")

    def _fixed_immutables(self, current, proposed):
        if current.id != proposed.id:
            raise NotSavedError("id cannot be modified")

        if current.created_at != proposed.created_at:
            raise NotSavedError("created_at cannot be modified")

        if current.created_by != proposed.created_by:
            raise NotSavedError("created_by cannot be modified")

    def _source_and_target_valid(self, link):
        if link.source is None or link.target is None:
            raise NotSavedError("source and target must be set")

        if not storage.has_item(link.source):
            raise NotSavedError("source must be a valid item id")

        if not storage.has_item(link.target):
            raise NotSavedError("target must be a valid item id")

        if link.source == link.target:
            raise NotSavedError("source and target must be different")

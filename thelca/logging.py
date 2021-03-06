import logging
from json import dumps
from thelca.time import current_time_UTC

class Event:
    def __init__(self, type, value, user):

        self.user = user
        self.type = type
        self.time = current_time_UTC()

        if value is not None:
            if isinstance(value, str):
                self.value = value
            elif 'search' in type:
                self.value = [x.id for x in value]
            else:
                self.value = vars(value)

    def json(self):
        return dumps(vars(self), sort_keys=True)

class EventLogger:

    def __init__(self, filename=None):
        if filename is not None:
            logging.basicConfig(filename=filename, format='%(message)s')

    def server_start(self, config):
        event = Event("Server started", config, "system")
        logging.critical(event.json())

    def server_stop(self):
        event = Event("Server stopped", None, "system")
        logging.critical(event.json())

    def service_read(self, service, user):
        event = Event("Service read", service, user)
        logging.critical(event.json())

    def item_created(self, item, user):
        event = Event("Item created", item, user)
        logging.critical(event.json())

    def item_read(self, item, user):
        event = Event("Item read", item.id, user)
        logging.critical(event.json())

    def item_updated(self, old_item, new_item, user):
        event = Event("Item updated", new_item, user)
        logging.critical(event.json())

    def item_search(self, items, user):
        event = Event("Item search", items, user)
        logging.critical(event.json())

    def link_created(self, link, user):
        event = Event("Link created", link, user)
        logging.critical(event.json())

    def link_read(self, link, user):
        event = Event("Link read", link.id, user)
        logging.critical(event.json())

    def link_updated(self, old_link, new_link, user):
        event = Event("Link updated", new_link, user)
        logging.critical(event.json())

    def link_deleted(self, link, user):
        event = Event("Link deleted", link.id, user)
        logging.critical(event.json())

    def link_search(self, links, user):
        event = Event("Link search", links, user)
        logging.critical(event.json())

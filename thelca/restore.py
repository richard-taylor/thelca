from json import loads
from thelca.model import Item, Link

import thelca.api

def from_event_log(filename):
    with open(filename) as events:
        for line in events:
            json = loads(line)
            type = json['type']

            if type == 'Item created':
                item = Item()
                item.__dict__.update(json['value'])
                thelca.api.storage.save_item(item)

            elif type == 'Item updated':
                item = Item()
                item.__dict__.update(json['value'])
                thelca.api.storage.modify_item(None, item)

            elif type == 'Link created':
                link = Link()
                link.__dict__.update(json['value'])
                thelca.api.storage.save_link(link)

            elif type == 'Link updated':
                link = Link()
                link.__dict__.update(json['value'])
                thelca.api.storage.modify_link(None, link)

            elif type == 'Link deleted':
                link = Link()
                link.__dict__.update(json['value'])
                thelca.api.storage.remove_link(link)

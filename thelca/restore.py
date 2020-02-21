from json import loads
from thelca.model import Item

import thelca.api

def from_event_log(filename):
    with open(filename) as events:
        for line in events:
            json = loads(line)
            type = json['type']
            if type == 'Item created' or type == 'Item updated':
                item = Item()
                item.__dict__.update(json['value'])

                thelca.api.storage.save_item(item)

from thelca.error import ItemNotFound, LinkNotFound

class MemoryStore:
    def __init__(self):
        self.items = {}
        self.links = {}

    def find_item(self, id):
        try:
            return self.items[id]
        except KeyError:
            raise ItemNotFound()

    def find_items(self, key, value):
        return [i for i in self.items.values() if i.properties.get(key) == value]

    def has_item(self, id):
        return id in self.items

    def save_item(self, item):
        self.items[item.id] = item

    def modify_item(self, new_item):
        self.items[new_item.id] = new_item

    def find_link(self, id):
        try:
            return self.links[id]
        except KeyError:
            raise LinkNotFound()

    def save_link(self, link):
        self.links[link.id] = link

    def modify_link(self, new_link):
        self.links[new_link.id] = new_link

    def remove_link(self, id):
        self.links.pop(id, None)

    def find_links_source(self, id):
        return [x for x in self.links.values() if x.source == id]

    def find_links_target(self, id):
        return [x for x in self.links.values() if x.target == id]

    def find_links_either(self, id):
        return [x for x in self.links.values() if x.source == id or x.target == id]

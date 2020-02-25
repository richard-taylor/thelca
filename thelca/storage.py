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

    def has_item(self, id):
        return id in self.items

    def save_item(self, item):
        self.items[item.id] = item

    def modify_item(self, old_item, new_item):
        self.items[new_item.id] = new_item

    def find_link(self, id):
        try:
            return self.links[id]
        except KeyError:
            raise LinkNotFound()

    def save_link(self, link):
        self.links[link.id] = link

    def modify_link(self, old_link, new_link):
        self.links[new_link.id] = new_link

    def remove_link(self, link):
        self.links.pop(link.id, None)

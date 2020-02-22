from thelca.error import ItemNotFound

class MemoryStore:
    def __init__(self):
        self.items = {}

    def find_item(self, id):
        try:
            return self.items[id]
        except KeyError:
            raise ItemNotFound()

    def save_item(self, item):
        self.items[item.id] = item

    def modify_item(self, old_item, new_item):
        self.items[new_item.id] = new_item

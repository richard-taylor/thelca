class MemoryStore:
    def __init__(self):
        self.items = {}

    def find_item(self, id):
        try:
            return self.items[id]
        except KeyError:
            return None

    def save_item(self, item):
        self.items[item.id] = item

import uuid
from thelca.time import current_time_UTC

class Trackable:
    def __init__(self, created_by):
        if created_by is None:
            self.id = None
            self.created_by = None
            self.created_at = None
        else:
            self.id = str(uuid.uuid4())
            self.created_by = created_by
            self.created_at = current_time_UTC()

class Item(Trackable):
    def __init__(self, created_by = None, properties = None):
        super().__init__(created_by)
        self.properties = properties

class Link(Trackable):
    def __init__(self, created_by = None, src = None, dest = None, properties = None):
        super().__init__(created_by)
        self.src = None if src is None else src.id
        self.dest = None if dest is None else dest.id
        self.properties = properties

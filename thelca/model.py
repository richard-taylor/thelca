import datetime
import uuid

class Trackable:
    def __init__(self, created_by):
        if created_by is None:
            self.id = None
            self.created_by = None
            self.created_at = None
        else:
            self.id = str(uuid.uuid4())
            self.created_by = created_by.id
            self.created_at = datetime.datetime.utcnow().isoformat()

class Item(Trackable):
    def __init__(self, created_by = None, type = None, properties = None):
        super().__init__(created_by)
        self.type = type
        self.properties = properties

class Link(Trackable):
    def __init__(self, created_by = None, type = None, src = None, dest = None):
        super().__init__(created_by)
        self.type = type
        self.src = None if src is None else src.id
        self.dest = None if dest is None else dest.id

class User(Trackable):
    def __init__(self, created_by = None):
        super().__init__(created_by)
        if created_by is None:
            self.id = 'root'

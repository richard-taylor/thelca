from datetime import datetime, timezone
import uuid

class Trackable:
    def __init__(self, created_by):
        if created_by is None:
            self.id = None
            self.created_by = None
            self.created_at = None
        else:
            self.mark_creation(created_by)

    def mark_creation(self, creator):
        self.id = str(uuid.uuid4())
        self.created_by = creator.id
        self.created_at = datetime.now(timezone.utc).isoformat()

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

class User(Trackable):
    def __init__(self, created_by = None):
        super().__init__(created_by)
        if created_by is None:
            self.id = 'root'

class NotAuthorisedError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ItemNotFound(NotFoundError):
    pass

class LinkNotFound(NotFoundError):
    pass

class NotSavedError(Exception):
    pass

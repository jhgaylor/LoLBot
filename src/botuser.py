
class User(object):
    """
    Wrapper around a chat user

    # TODO: Add admin flag
    # TODO: add banned flag
    """

    def __init__(self, id, **options):
        self.id = id
        self.options = options

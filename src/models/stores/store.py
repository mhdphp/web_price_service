

class Store(object):

    def __init__(self, name, url_prefix):
        self.name = name
        self.url_prefix = url_prefix

    # string representation
    def __repr__(self):
        return "<Store {}".format(self.name)
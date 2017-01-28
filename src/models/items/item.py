

class Alert(object):

    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

    # string representation
    def __repr__(self):
        return "<Item {} with URL {}".format(self.name, self.url)
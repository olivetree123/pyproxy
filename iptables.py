class Step(object):

    def __init__(self, name):
        self.name = name

    def add_rule(self, ):
        pass


class IPTables(object):

    def __init__(self):
        self.prerouting = Step(name="prerouting")
        self.postrouting = Step(name="postrouting")
        self.input = Step(name="input")
        self.output = Step(name="output")
        self.forward = Step(name="forward")

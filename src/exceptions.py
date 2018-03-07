class ExteralIdDistributionError(Exception):

    def message(self):
        return self.args[0]


class TypeError(ExteralIdDistributionError):

    def __init__(self, name, allow=None, got=None):
        self.name = name
        self.allow = allow
        self.got = got

    def message(self):
        if self.allow:
            return self.name + ' type must be one of: ' + ', '.join(sorted(self.allow))
        elif self.got is None:
            return self.name + 'is is missing'
        else:
            return 'invalid ' + self.name
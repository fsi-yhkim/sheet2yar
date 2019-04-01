class ImporterBase(object):
    name = ''
    name_verbose = ''
    _arguments = None

    def __init__(self, arguments, *args, **kwargs):
        self._arguments = arguments

    def load(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def add_subparser(cls, argument_parser):
        raise NotImplementedError

from .shell import Shell
from .auth import Auth
from .gen import Gen

class Pynecone(Shell):

    def __init__(self):
        super().__init__('pynecone')

    def get_commands(self):
        return [Auth(), Gen()]

    def add_arguments(self, parser):
        pass

    def get_help(self):
        return 'pynecone shell'
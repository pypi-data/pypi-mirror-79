import importlib.util
from .cmd import Cmd


class Run(Cmd):

    def get_help(self):
        return 'run a python script'

    def add_arguments(self, parser):
        parser.add_argument('script_path', help="path to the script to be executed")
        parser.add_argument('func_name', help="name of the function in the script to be executed")
        parser.add_argument('args', help="arguments", nargs='+')

    def run(self, args):
        self.load_script(args.script_path, args.func_name)(args.args)

    @classmethod
    def get_handler(cls, file, callback):
        spec = importlib.util.spec_from_file_location('testmod', file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def handler():
            getattr(module, callback)

        return handler

    @classmethod
    def load_script(cls, script_path, func_name):
        return cls.get_handler(script_path, func_name)

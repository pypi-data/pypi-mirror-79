import importlib.util
from .command import Command


class ScriptCommand(Command):

    def get_help(self):
        return 'run a python script'

    def add_arguments(self, parser):
        parser.add_argument('script_path', help="path to the script to be executed")
        parser.add_argument('func_name', help="name of the function in the script to be executed")

    def run(self, args):
        self.load_script(args.script_path, args.func_name, args)

    @classmethod
    def get_handler(cls, file, callback, cmdargs):
        spec = importlib.util.spec_from_file_location('testmod', file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def handler(*args):
            t = tuple(list(args) + [cmdargs])
            getattr(module, callback)(t)

        return handler

    @classmethod
    def load_script(cls, script_path, func_name, cmdargs):
        return cls.get_handler(script_path, func_name, cmdargs)
import importlib.util

class ScriptCommand:

    def get_handler(self, file, callback):
        spec = importlib.util.spec_from_file_location('testmod', file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def handler(args):
            getattr(module, callback)(args)

        return handler
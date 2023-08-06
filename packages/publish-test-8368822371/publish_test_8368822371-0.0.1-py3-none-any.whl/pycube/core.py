from pycube.memory.state import State

class Core(State):
    def __init__(self, **kwargs):
        State.__init__(self, state=kwargs.get('state'), **kwargs)
        self.modules = {}
        self.transitive_methods = {}

    def add_module(self, name, module):
        self.modules[name] = module
        for method_name in module.transitive_methods:
            def helper(method_name=method_name):
                return lambda *args, **kwargs: module.transitive_methods[method_name](module, *args, **kwargs)
            setattr(self, method_name, helper(method_name))
        return self

    def call_module(self, name, function, *args, **kwargs):
        return getattr(self.modules[name], function)(*args, **kwargs)

    def remove_module(self, module):
        del self.modules[module.name]
        return self

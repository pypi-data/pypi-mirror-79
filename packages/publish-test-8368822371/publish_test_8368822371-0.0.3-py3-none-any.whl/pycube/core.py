from pycube.memory.state import State

class Core(State):
    def __init__(self, **kwargs):
        State.__init__(self, state=kwargs.get('state'), **kwargs)
        self.modules = {}
        self.transitive_methods = {}

    def __helper(self, method_name):
        method = self.transitive_methods[method_name]
        instance = self.modules[method['instance']]
        function = method['function']
        return lambda *args, **kwargs: function(instance, *args, **kwargs)

    def add_module(self, name, module):
        transitive_methods = module._call_expose()
        for method_name in transitive_methods:
            if not self.modules.get(module.name):
                self.modules[module.name] = {}
            self.modules[name] = module
            self.transitive_methods[method_name] = {'instance': name, 'function': transitive_methods[method_name]}
            setattr(self, method_name, self.__helper(method_name))
        return self

    def call_module(self, name, function, *args, **kwargs):
        return getattr(self.modules[name], function)(*args, **kwargs)

    def remove_module(self, module):
        del self.modules[module.name]
        return self

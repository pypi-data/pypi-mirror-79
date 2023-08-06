import re
from pycube.memory.state import State

class Module(State):
    def __init__(self, **kwargs):
        State.__init__(self, state=kwargs.get('state'), **kwargs)
        self.name = (kwargs.get('name') or self.__class__.__name__).lower()
        self.transitive_methods = {}
        
    def add_io(self, io):
        setattr(self, io.name, io.request)
        return self

    def remove_io(self, name):
        delattr(self, name)
        return self

    def expose(self):
        pass # Override to include methods that will propagate to core

    def _call_expose(self):
        self.expose()
        return self.transitive_methods

    def transitive(self):
        def decorator(function, *args, **kwargs):
            self.transitive_methods[function.__name__] = function
            return function
        return decorator
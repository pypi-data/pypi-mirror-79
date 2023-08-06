from pycube.memory.state import State

class Module(State):
    transitive_methods = {}

    def __init__(self, **kwargs):
        State.__init__(self, state=kwargs.get('state'), **kwargs)
        self.name = (kwargs.get('name') or self.__class__.__name__).lower()

    def add_io(self, io):
        setattr(self, io.name, io.request)
        return self

    def remove_io(self, name):
        delattr(self, name)
        return self

    @classmethod        
    def transitive(cls, name=None):
        def decorator(function, *args, **kwargs):
            cls.transitive_methods[name or function.__name__] = function
            return function
        return decorator
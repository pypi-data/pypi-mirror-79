class State:
    def __init__(self, state=None, **kwargs):
        self.memory = state or {}

    def get_state(self, key):
        return self.memory.get(key)

    def set_state(self, key, value):
        self.memory[key] = value

    def wipe_state(self, key, state=None):
        state = state or self.memory
        del state[key]

    def list_state(self, key, cb, **kwargs):
        results = []
        for value in self.get(key):
            result = cb(value, **kwargs)
            results.append(result)
        return results

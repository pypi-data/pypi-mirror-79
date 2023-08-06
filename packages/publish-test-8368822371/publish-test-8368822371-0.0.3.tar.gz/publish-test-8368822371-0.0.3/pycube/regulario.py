from pycube.memory.state import State

class RegularIO(State):
    def __init__(self, *args, **kwargs):
        State.__init__(self, state=kwargs.get('state'), **kwargs)
        self.name = (kwargs.get('name') or self.__class__.__name__).lower()

    def request_handler(self, params, **kwargs):
        pass # Override to perform action

    def response_handler(self, params, **kwargs):
        pass # Override to perform action

    def process_handler(self, params, **kwargs):
        pass # Override to perform action

    def params_transformer(self, *args, **kwargs):
        return args

    def param_handler(self, params, **kwargs):
        return params

    def _call_params_transformer(self, *args, **kwargs):
        return self.params_transformer(*args, **kwargs)

    def _call_params(self, params, **kwargs):
        _params = self.param_handler(params, **kwargs)
        return _params or params

    def _call_request(self, params, **kwargs):
        params = self._call_params(params, **kwargs)
        return self.request_handler(params, **kwargs)

    def _call_process(self, params, **kwargs):
        return self.process_handler(params, **kwargs)

    def _call_response(self, params, **kwargs):
        params = self.param_handler(params, **kwargs)
        return self.response_handler(params, **kwargs)

    def request(self, *args, **kwargs):
        params = self._call_params_transformer(*args, **kwargs)
        kwargs["__request__"] = self._call_request(params, **{**kwargs, '__calltype__': 'request'})
        kwargs["__process__"] = self._call_process(params, **{**kwargs, '__calltype__': 'response'})
        return self._call_response(params, **kwargs)

import json
import re
import sys
import traceback
from aiohttp import web

class ApiGateway:
    name = None
    request_hooks = {'GET': {},'POST': {},'PUT': {},'PATCH': {},'DELETE': {},'OPTIONS': {}}

    @classmethod
    async def __generate_internal_payload(cls, request):
        query = {k: request.rel_url.query[k] for k in request.rel_url.query.keys()} if request.rel_url.query else None
        payload = await request.json() if request.can_read_body else None
        path_info = request.match_info if request.match_info else None
        return {
            'query': query, 
            'payload': payload, 
            'path_info': path_info, 
            'meta': {
                'handler': cls.name or cls.__name__, 
                'method': request.method,
                'path': request.path_qs
            }
        }

    @classmethod
    async def __internal_routing(cls, request):
        internal_payload = await cls.__generate_internal_payload(request)
        request_result = cls.__request_handler(internal_payload) 
        internal_payload = {**internal_payload, "result": request_result}
        return web.Response(body=json.dumps(internal_payload), content_type='application/json')

    @classmethod
    def __generate_internal_routing(cls, method, levels=26):
        paths = []; path = ''
        for i in range(levels):
            path += '/{lv'+ chr(i+65) +'}'
            paths.insert(0, getattr(web, method)(path, cls.__internal_routing))
            paths.insert(0, getattr(web, method)(path+'/', cls.__internal_routing))
        paths.append(getattr(web, method)('/', cls.__internal_routing))
        return paths

    @classmethod
    def __routes(cls, routes=[]):
        supported_methods = ['get','post','put','patch','delete','options']
        for method in supported_methods:
            routes += cls.__generate_internal_routing(method)
        cls.Hook.hooks()
        return routes

    @classmethod
    def __request_handler(cls, internal_payload):
        path_info = internal_payload['path_info']
        if not path_info: return None
        handler = cls.get_handler(path_info, internal_payload['meta']['method'])
        if not callable(handler): return None
        try:
            return {"success": handler(internal_payload)}
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return {
                'error': {
                    'exception': e.__class__.__name__,
                    'message': str(e),
                    'traceback': traceback.format_exception(exc_type, exc_value, exc_traceback)
                }
            }

    @classmethod
    def __get_hook(cls, path, handler):
        res = {}; ptr=res
        matches = re.findall(r"\/([^/]+)", path)
        for index, lv in enumerate(matches):
            ptr[lv]={} if index < len(matches)-1 else handler
            ptr=ptr[lv]
        return res

    @classmethod
    def get_handler(cls, path_info, method):
        ptr = cls.request_hooks[method]
        for lv in path_info:
            if not ptr.get(path_info[lv]): return None
            ptr = ptr[path_info[lv]]
        return ptr

    @classmethod
    def set_handler(cls, method, hook, ptr = None, pptr = None):
        ptr = ptr or cls.request_hooks[method]
        for lv in hook:
            if ptr.get(lv):
                return cls.set_handler(method, hook[lv], ptr[lv], pptr)
            ptr[lv] = {**hook[lv]} if hook[lv].__class__.__name__ != 'function' else hook[lv]
            

    @classmethod
    def add_request_hook(cls, method, path, handler):
        hook = cls.__get_hook(path, handler)
        cls.set_handler(method, hook)

    @classmethod
    def serve(cls, name=None, port=8080):
        cls.name = name
        app = web.Application()
        app.add_routes(cls.__routes())
        web.run_app(app, port=port)

    class Hook:
        def requests_hooking(self):
            pass # Override to hook the methods  

        def get(self, path, handler):
            return ApiGateway.Hook.__hook__('GET', path, handler)

        def post(self, path, handler):
            return ApiGateway.Hook.__hook__('POST', path, handler)

        def put(self, path, handler):
            return ApiGateway.Hook.__hook__('PUT', path, handler)

        def patch(self, path, handler):
            return ApiGateway.Hook.__hook__('PATCH', path, handler)      

        def delete(self, path, handler):
            return ApiGateway.Hook.__hook__('DELETE', path, handler)

        def option(self, path, handler):
            return ApiGateway.Hook.__hook__('OPTION', path, handler)

        @classmethod
        def hooks(cls):
            for kls in cls.__subclasses__():
                kls().requests_hooking()

        @staticmethod
        def __hook__(method, path, handler):
            return ApiGateway.add_request_hook(method, path, handler)

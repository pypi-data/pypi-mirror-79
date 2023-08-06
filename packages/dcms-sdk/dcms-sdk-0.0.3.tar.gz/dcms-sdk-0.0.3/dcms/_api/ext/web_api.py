# web_api


class WebApi:
    def __init__(self):
        self._apis = {}
        pass

    def __call__(self, name, method='default'):
        def temp(func):
            def get_func(request):
                pass

            def form_func(request):
                pass

            def json_func(request):
                pass

            def default_func(request):
                pass

            if method in ['GET', 'get']:
                func = get_func
            elif method in ['POST', 'post', 'POST_FORM', 'post_form']:
                func = form_func
            elif method in ['POST_JSON', 'post_json']:
                func = json_func

            self._apis[name] = {'func': func, 'method': method.upper()}

            # print(func, name, method)
            return default_func

        return temp

    def invoke(self, name, request):
        _api = self._apis.get(name)
        if not _api:
            return {'status': 5, 'msg': 'not found'}

        return _api.get('func')(request) or {'status': 0, 'msg': 'no result'}


web_api = WebApi()


@web_api('666', '123456')
def test():
    print('hello')
# def web_api(func, name, method=None):
#
#
#     if method == 'GET' or method == 'get':

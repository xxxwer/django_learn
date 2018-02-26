from inspect import signature
import functools
from freeLink.utils import error

def request_method_assert(method, response_type = 'html'):
    if method != 'POST' and method != 'GET':
        raise Exception('本装饰器只支持 post get 检查');
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            request = args[0]
            if method != request.method:
                return return_method_check_fail(request, response_type, method)
            return func(*args, **kw)
        return wrapper
    return decorator

def return_method_check_fail(request, response_type, method):
    if response_type == 'html':
        return error.show_error_1(request, Exception({'type': '请求参数错误', 'reason': '必须使用 '+ method +' 请求'}))
    else:
        return error.show_error_2(request, Exception({'type': '请求参数错误', 'reason': '必须使用 '+ method +' 请求'}))

if __name__ == '__main__':
    pass


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from var_dump import var_export
import logging

from freeLink.utils import debug
from freeLink.utils import error
from freeLink.utils.my_decorator import request_method_assert


logger = logging.getLogger('django')

@request_method_assert('POST')
def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('commonLink:keyword_list'))
    else:
        return error.show_error_html(request, Exception({'type': '登录失败', 'reason': '用户不存在或者密码错误'}))

def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('commonLink:keyword_list'))
    return render(request, 'commonLink/login.html')

def do_logout(request):
    request.session.clear()
    logout(request)
    return redirect(reverse('my_login_page'))

from var_dump import var_export
from django.http import HttpResponse

def my_var_dump(var):
    return HttpResponse(content=var_export(var))
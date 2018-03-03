from django.shortcuts import render
from django.http import HttpResponse
import json

def show_error_html(request, e):
    if isinstance(e.args[0], dict) and e.args[0]['type'] and e.args[0]['reason']:
        return render(request, 'error_1.html', {'title': e.args[0]['type'], 'content': e.args[0]['reason']}, None, 400)
    else:
        return render(request, 'error_1.html', {'title': '不明错误，请联系管理员', 'content': str(e)}, None, 400)

def show_error_json(request, e):
    if isinstance(e.args[0], dict) and e.args[0]['type'] and e.args[0]['reason']:
        return HttpResponse(json.dumps({'status': 'failed', 'reason': e.args[0]['reason']}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': 'failed', 'reason': str(e)}), content_type="application/json")

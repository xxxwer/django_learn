# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from commonLink import models
from commonLink.repo import esRepo
from freeLink.utils import error
import json
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required


class ESIndexAll(View):
    def get(self, request):
        kcEs = esRepo.KeywordContentES()
        return HttpResponse(json.dumps(kcEs.indexAll()), content_type='application/json')


@login_required
def search_keyword(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': '搜索 必须使用 post 请求'})
        kcEs = esRepo.KeywordContentES()
        es_result = kcEs.searchKeyword(request.POST.get('keyword', None))
        return render(request, 'commonLink/esSearchKeyword.html', {'es_result': json.dumps(es_result)})
    except Exception as e:
        return error.show_error_html(request, e)

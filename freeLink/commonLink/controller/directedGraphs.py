# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from commonLink import models
from commonLink.repo import esRepo
from freeLink.utils import error
import json
from django.views.generic.base import View


class StrongConnectivity(View):
    def get(self, request):
        kcEs = esRepo.KeywordContentES()
        return HttpResponse(json.dumps(kcEs.indexAll()), content_type='application/json')


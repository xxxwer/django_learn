# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template import loader

from . import models
from freeLink.utils.debug import my_var_dump
from .repo import keywordContentRepo
from freeLink.utils import error
from .forms import UploadForm


@login_required
def index(request):
    keyword_list = models.keyword.objects.all().order_by('-click_number')
    paginator = Paginator(keyword_list, 15)

    page = request.GET.get('page')
    try:
        keywords = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        keywords = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        keywords = paginator.page(paginator.num_pages)

    return render(request, 'commonLink/linkList.html', {'keywords': keywords})


@login_required
def detail(request, id_keyword):
    try:
        if int(id_keyword) == 0:
            raise Exception({'type': '请求参数错误', 'reason': 'root 节点不能访问'})
        data = {}
        data['keyword_content'] = keywordContentRepo.get_keyword_content(id_keyword)
        data['parent_keyword'] = keywordContentRepo.get_parent_keyword(id_keyword)
        data['brother_keyword'] = keywordContentRepo.get_brother_keyword(id_keyword, data['parent_keyword'].id)
        data['child_keyword'] = keywordContentRepo.get_child_keyword(id_keyword)
        data['extra_keyword'] = keywordContentRepo.get_extra_keyword(id_keyword)
        data['page_data'] = json.dumps({'keyword_is_private': data['keyword_content']['keyword'].is_private})

        keywordContentRepo.countKeywordClick(data['keyword_content']['keyword'])
        return render(request, 'commonLink/linkDetail.html', data)
    except Exception as e:
        return error.show_error_html(request, e)


@login_required
def detail_update(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': '修改 必须使用 post 请求'})
        id_keyword = request.POST.get('id_keyword', None)
        keyword = request.POST.get('keyword', None)
        content = request.POST.get('content', 'null')
        keywordContentRepo.update_keyword_content(id_keyword, keyword, content)
        # return redirect(reverse('commonLink:keyword_detail', args=(id_keyword,)))
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    except Exception as e:
        # return error.show_error_html(request, e)
        return error.show_error_json(request, e)


@login_required
def ajax_search_keyword(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': 'ajax 必须使用 post 请求'})
        keywords = keywordContentRepo.search_keyword(request.POST.get('keyword', None))
        btnClass = request.POST.get('btnClass', 'updateParentBtn')
        t = loader.get_template('commonLink/ajaxSearchKeyword.html')
        view_string = t.render({'keywords': keywords, 'btnClass': btnClass}, request)

        return HttpResponse(json.dumps({'status': 'success', 'html': view_string}), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)


@login_required
def ajax_update_parent(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': 'ajax 必须使用 post 请求'})
        id_keyword_parent = request.POST.get('id_keyword_parent', None)
        id_keyword = request.POST.get('id_keyword', None)
        keywordContentRepo.update_keyword_keyword(id_keyword_parent, id_keyword)
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)


@login_required
def ajax_add_child(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': 'ajax 必须使用 post 请求'})
        id_keyword_parent = request.POST.get('id_keyword_parent', None)
        keyword = request.POST.get('keyword', None)
        content = request.POST.get('content', None)
        keyword_obj = models.keyword()
        keyword_obj.keyword = keyword
        keyword_obj.click_number = 0
        keyword_obj.save()
        keywordContentRepo.update_keyword_content(keyword_obj.id, keyword, content)
        keywordContentRepo.update_keyword_keyword(id_keyword_parent, keyword_obj.id)
        new_keyword_url = reverse('commonLink:keyword_detail', args=(keyword_obj.id,))
        return HttpResponse(json.dumps({'status': 'success', 'new_keyword_url': new_keyword_url}), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)


@login_required
def ajax_add_extra_link(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': 'ajax 必须使用 post 请求'})
        id_keyword_1 = request.POST.get('id_keyword_1', None)
        id_keyword_2 = request.POST.get('id_keyword_2', None)
        desc = request.POST.get('desc', None)
        keywordContentRepo.add_extra_keyword(id_keyword_1, id_keyword_2, desc)
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)


@login_required
def delete_extra_link(request):
    try:
        id_keyword_1 = request.POST.get('id_keyword_1', None)
        id_keyword_2 = request.POST.get('id_keyword_2', None)
        keywordContentRepo.del_extra_keyword(id_keyword_1, id_keyword_2)
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)


@login_required
def search_keyword(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': '搜索 必须使用 post 请求'})
        keywords = keywordContentRepo.search_keyword(request.POST.get('keyword', None))
        return render(request, 'commonLink/searchKeyword.html', {'keywords': keywords})
    except Exception as e:
        return error.show_error_html(request, e)


@login_required
def list_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = models.UploadFile(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect(reverse('commonLink:upload_file'))
    else:
        form = UploadForm() # A empty, unbound form

    # Load documents for the list page
    uploadfiles = models.UploadFile.objects.all().order_by('-id')
    paginator = Paginator(uploadfiles, 15)

    page = request.GET.get('page')
    try:
        uploadfiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        uploadfiles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        uploadfiles = paginator.page(paginator.num_pages)

    # Render list page with the documents and the form
    return render(request, 'commonLink/upload_list.html', {'documents': uploadfiles, 'form': form})


@login_required
def keyword_private(request):
    try:
        if request.method != 'POST':
            raise Exception({'type': '请求参数错误', 'reason': '搜索 必须使用 post 请求'})
        keywordContentRepo.setKeywordPrivate(request.POST.get('id_keyword', None), request.POST.get('private', 0))
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)

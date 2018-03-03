from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.views.decorators.csrf import csrf_exempt
from freeLink.utils import error
from commonLink import models
from commonLink.repo import keywordContentRepo


@csrf_exempt
def rankingList(request):
    keyword_list = models.keyword.objects.filter(is_private=0).order_by('-click_number')
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

    k_array = [{
        'id': x.id,
        'keyword': x.keyword,
        'click_number': x.click_number
        } for x in keywords]

    data = {
        'count': paginator.count,
        'now_page': keywords.number,
        'num_pages': paginator.num_pages,
        'keywords': k_array,
        'has_previous': keywords.has_previous(),
        'has_next': keywords.has_next(),
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def keywordDetail(request):
    id_keyword = request.GET.get('id_keyword')
    try:
        if int(id_keyword) == 0:
            raise Exception({'type': '请求参数错误', 'reason': 'root 节点不能访问'})
        keyword = keywordContentRepo.get_keyword(id_keyword)
        if keyword.is_private == 1:
            raise Exception({'type': '请求参数错误', 'reason': '该节点不存在'})

        data = {}
        temp = keywordContentRepo.get_keyword_content(id_keyword)
        data['keyword_content'] = {k: temp[k].to_dict() for k in temp}

        temp = keywordContentRepo.get_parent_keyword(id_keyword)
        data['parent_keyword'] = [temp.to_dict()]

        temp = keywordContentRepo.get_brother_keyword(id_keyword, data['parent_keyword'][0]['id'])
        data['brother_keyword'] = [x.to_dict() for x in temp]

        temp = keywordContentRepo.get_child_keyword(id_keyword)
        data['child_keyword'] = [x.to_dict() for x in temp]


        keywordContentRepo.countKeywordClick(keyword)

        return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)


@csrf_exempt
def search_keyword(request):
    try:
        keywords = keywordContentRepo.search_keyword(request.GET.get('keyword', None)).filter(is_private=0)[0:20]
        keywords = [x.to_dict() for x in keywords]

        return HttpResponse(json.dumps({'searched': keywords}), content_type="application/json")
    except Exception as e:
        return error.show_error_json(request, e)

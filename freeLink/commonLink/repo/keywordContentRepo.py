from commonLink import models
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from freeLink.utils.debug import my_var_dump

def get_keyword(id_keyword):
    try:
        keyword = models.keyword.objects.get(id=id_keyword)
        return keyword
    except ObjectDoesNotExist:
        raise Exception({'type': '请求参数错误', 'reason': '错误，没有该 id_keyword: ' + str(id_keyword)})


def get_keyword_content(id_keyword):
    keyword = get_keyword(id_keyword)
    try:
        keyword_content = models.keywordContent.objects.get(id_keyword=int(id_keyword))
        if keyword_content.id_content:
            content = models.content.objects.get(pk=keyword_content.id_content)
    except ObjectDoesNotExist:
        content = models.content()
        keyword_content = models.keywordContent()

    return {'keyword': keyword, 'content': content, 'keyword_content': keyword_content}


def get_parent_keyword(id_keyword):
    try:
        keyword_keyword = models.keywordkeyword.objects.get(id_keyword=int(id_keyword))
        if keyword_keyword:
            parent_keyword = get_keyword(keyword_keyword.id_keyword_parent)
    except ObjectDoesNotExist:
        parent_keyword = None
    return parent_keyword


def get_child_keyword(id_keyword):
    child_keyword_ids = models.keywordkeyword.objects.filter(id_keyword_parent=int(id_keyword))
    child_keyword = []
    for id_obj in child_keyword_ids:
        child_keyword.append(get_keyword(id_obj.id_keyword))
    return child_keyword


def get_brother_keyword(id_keyword, id_keyword_parent=None):
    if not id_keyword_parent:
        parent_keyword = get_parent_keyword(id_keyword)
        id_keyword_parent = parent_keyword.id

    brother_keyword = get_child_keyword(id_keyword_parent)
    if not brother_keyword:
        raise Exception({'type': '请求参数错误', 'reason': '一定存在至少一个兄弟节点，该节点为自己本身'})
    return brother_keyword


def filter_two_parent_keyword():
    all_keyword = models.keyword.objects.all()
    for k in all_keyword:
        ids = models.keywordkeyword.objects.filter(id_keyword=int(k.id))
        if len(ids) != 1:
            print(k.id)


def update_keyword_content(id_keyword, keyword, content):
    keyword_content = get_keyword_content(id_keyword)
    if not keyword:
        raise Exception({'type': '请求参数错误', 'reason': 'keyword不能为空'})
    keyword_content['keyword'].keyword = keyword
    keyword_content['keyword'].save()

    if (not keyword_content['keyword_content'].id) and (not keyword_content['content'].id):
        keyword_content['content'].content = content
        keyword_content['content'].save()
        keyword_content['keyword_content'].id_keyword = id_keyword
        keyword_content['keyword_content'].id_content = keyword_content['content'].id
        keyword_content['keyword_content'].save()
        return

    if keyword_content['keyword_content'].id and keyword_content['content'].id:
        keyword_content['content'].content = content
        keyword_content['content'].save()
        return

    raise Exception({'type': '系统错误', 'reason': '该keyword 存储数据不正确 id_keyword:' + id_keyword})


def search_keyword(keyword):
    if not keyword:
        raise Exception({'type': '请求参数错误', 'reason': '关键字不能为空'})
    return models.keyword.objects.filter(keyword__contains=keyword).order_by('-click_number')


def update_keyword_keyword(id_keyword_parent, id_keyword):
    checkInt(id_keyword)
    checkInt(id_keyword_parent)
    if id_keyword == id_keyword_parent:
        raise Exception({'type': '请求参数错误', 'reason': '不能以自己为父节点'})
    try:
        keyword_keyword = models.keywordkeyword.objects.get(id_keyword=int(id_keyword))
    except ObjectDoesNotExist:
        keyword_keyword = models.keywordkeyword()

    keyword_keyword.id_keyword = id_keyword
    keyword_keyword.id_keyword_parent = id_keyword_parent
    keyword_keyword.save()

    parent_keyword = get_keyword(id_keyword_parent)
    keyword = get_keyword(id_keyword)
    if keyword.is_private != parent_keyword.is_private:
        keyword.is_private = parent_keyword.is_private
        keyword.save()


def checkInt(param):
    if isinstance(param, int):
        return
    if int(param):
        return


def get_extra_keyword(id_keyword):
    extra_keyword_link = models.keywordExtraLink.objects.filter(id_keyword_1=int(id_keyword))
    extra_keyword = {}
    extra_keyword_links = {}
    for obj in extra_keyword_link:
        extra_keyword[obj.id_keyword_2] = get_keyword(obj.id_keyword_2)
        extra_keyword[obj.id_keyword_2].extra_link = obj
    return extra_keyword


def add_extra_keyword(id_keyword_1, id_keyword_2, desc):
    ke1 = models.keywordExtraLink()
    ke2 = models.keywordExtraLink()
    ke1.id_keyword_1 = id_keyword_1
    ke1.id_keyword_2 = id_keyword_2
    ke1.desc = desc
    ke2.id_keyword_1 = id_keyword_2
    ke2.id_keyword_2 = id_keyword_1
    ke2.desc = desc

    ke1.save()
    ke2.save()


def del_extra_keyword(id_keyword_1, id_keyword_2):
    extra_keyword_link = models.keywordExtraLink.objects.filter(id_keyword_1=int(id_keyword_1), id_keyword_2=int(id_keyword_2))
    extra_keyword_link.delete()
    extra_keyword_link = models.keywordExtraLink.objects.filter(id_keyword_1=int(id_keyword_2), id_keyword_2=int(id_keyword_1))
    extra_keyword_link.delete()


def countKeywordClick(keyword):
    if not isinstance(keyword, models.keyword):
        raise Exception({'type': '逻辑错误', 'reason': '错误，要传入 keyword model 类'})

    with connection.cursor() as cursor:
        cursor.execute('UPDATE `commonLink_keyword` SET `click_number` = `click_number`+1 WHERE id = %(id)s;', {'id':keyword.id})
    return

def doSetKeywordPrivate(keyword, zeroOrOne):
    keyword.is_private = zeroOrOne
    keyword.save()

def setKeywordPrivate(keyword, zeroOrOne, recursion=True):
    checkInt(zeroOrOne)
    if not isinstance(keyword, models.keyword):
        keyword = get_keyword(keyword)

    doSetKeywordPrivate(keyword, zeroOrOne)
    if not recursion:
        return
    child_keywords = get_child_keyword(keyword.id)
    for keyword in child_keywords:
        setKeywordPrivate(keyword, zeroOrOne)
    return

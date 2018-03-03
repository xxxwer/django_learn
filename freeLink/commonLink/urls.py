"""freeLink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from commonLink.controller import es, other, login, api
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # free link 系统链接
    url(r'^$', views.index, name='keyword_list'),
    url(r'^index/$', views.index, name='keyword_list_orderby_clicknum'), #url字符串最后加个 ‘／’
    url(r'^detail/(?P<id_keyword>[0-9]+)/$', views.detail, name='keyword_detail'),
    url(r'^detail/update/$', views.detail_update, name='update_keyword'),
    url(r'^ajax/search_keyword/$', views.ajax_search_keyword, name='ajax_search_keyword'),
    url(r'^ajax/update_parent_keyword/$', views.ajax_update_parent, name='ajax_update_parent_keyword'),
    url(r'^ajax/add_child_keyword/$', views.ajax_add_child, name='ajax_add_child_keyword'),
    url(r'^ajax/add_extra_link/$', views.ajax_add_extra_link, name='ajax_add_extra_link'),
    url(r'^ajax/del_extra_link/$', views.delete_extra_link, name='ajax_del_extra_link'),
    url(r'^search/keywordlist/$', views.search_keyword, name='search_keyword'),

    # 设置私人 标记
    url(r'^ajax/set_keyword_private/$', views.keyword_private, name='keyword_private'),
    # free link 的 es操作
    url(r'^es/indexAll/$', login_required(es.ESIndexAll.as_view()), name='es_index_all'),
    url(r'^es/search/$', es.search_keyword, name='es_search'),
    # 其他实验
    url(r'^other_app/$', other.otherAjax, name='other_app'),
    # 上传文件
    url(r'^upload_file/$', views.list_upload, name='upload_file'),
    # 登录
    url(r'^my_do_login/$', login.do_login, name='my_do_login'),
    url(r'^my_do_logout/$', login.do_logout, name='my_do_logout'),

    # api 数据
    url(r'^api/ranking/list/$', api.rankingList, name='api_rankingList'),
    url(r'^api/keyword/detail/$', api.keywordDetail, name='api_keywordDetail'),
    url(r'^api/keyword/search/$', api.search_keyword, name='api_searchkeyword')
]

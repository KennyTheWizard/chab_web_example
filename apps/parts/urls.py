from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getnewform$', views.get_new_part_form, name='newform'),
    url(r'^create/$', views.create_new_part, name='createpart'),
    url(r'^(?P<part_id>\d+)/update/$', views.update_part, name='updatepart'),
    url(r'^(?P<part_id>\d+)/edit$', views.get_part_edit_form, name='editpart'),
    url(r'^getparts/$', views.search_for_part_name_json, name='namesearch'),
    url(r'^getpartlist$', views.get_part_list, name='flatpartlist'),
    url(r'addchild/$', views.add_child, name='addchild'),
    url(r'^removechild/$', views.remove_child, name='remove_child'),
    url(r'deletepart/', views.delete_part, name='deletepart'),
]
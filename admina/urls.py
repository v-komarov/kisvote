from django.conf.urls import patterns, include, url
from	django.contrib.staticfiles.urls	import	staticfiles_urlpatterns
from	django.conf	import	settings


from admina.views import ReadAll, Groups, DelAccessAll, DelGroupData, ChAuthor



urlpatterns = [
    url(r'readall', ReadAll),
    url(r'groups', Groups),
    url(r'author', ChAuthor),
    url(r'delaccessall', DelAccessAll),
    url(r'delgroupdata', DelGroupData)

]
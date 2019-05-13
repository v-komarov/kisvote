from django.conf.urls import patterns, include, url
from	django.contrib.staticfiles.urls	import	staticfiles_urlpatterns
from	django.conf	import	settings


from admina.views import ReadAll, Groups, DelAccessAll



urlpatterns = [
    url(r'readall', ReadAll),
    url(r'groups', Groups),
    url(r'delaccessall', DelAccessAll)

]
from django.conf.urls import patterns, include, url
from	django.contrib.staticfiles.urls	import	staticfiles_urlpatterns
from	django.conf	import	settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kis.views.home', name='home'),
    # url(r'^kis/', include('kis.foo.urls')),

    url(r'^$', 'start.views.Home', name='Home'),
    url(r'^exit/$', 'start.views.Exit', name='Exit'),


    url(r'^contract/$', 'contract.views.List', name='List'),
    url(r'^tovote/$', 'contract.views.ToVote', name='ToVote'),    
    url(r'^newcontract/$', 'contract.views.New', name='New'),
    url(r'^contractopt/$', 'contract.views.Opt', name='Opt'),
    url(r'^personresult/$', 'contract.reports.PersonResult'),
    url(r'^editcontract/$', 'contract.views.EditPage1', name='EditPage1'),
    url(r'^page2contract/$', 'contract.page2.Page2', name='Page2'),
    url(r'^page3contract/$', 'contract.page3.Page3', name='Page3'),
    url(r'^page4contract/$', 'contract.page4.Page4', name='Page4'),
    url(r'^page5contract/$', 'contract.page5.Page5', name='Page5'),
    url(r'^page6contract/$', 'contract.page6.Page6', name='Page6'),
    url(r'^page7contract/$', 'contract.page7.Page7', name='Page7'),
    url(r'^page8contract/$', 'contract.page8.Page8', name='Page8'),

    url(r'^admina/', include('admina.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'css/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/task/kis/kis/static/css/',}),
    url(r'js/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/task/kis/kis/static/js/',}),
    url(r'fonts/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/task/kis/kis/static/fonts/',}),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

#coding:utf-8
from django.shortcuts import render
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response
from	django.http	import	HttpResponseRedirect


from kis.lib.userdata import AccessAdmin
from kis.lib.admina import GetGroupsData, GetAccessAll, DelReadAll, DelUserGroup, AddReadAll, AddUserGroup
from admina.forms import UserForm, GroupsForm



### --- Интерфейс отметки доступ для всех заявок ---
def	ReadAll(request):




    ### --- Проверка доступа к этой закладки ---
    if AccessAdmin(request) != 'OK':
        c = RequestContext(request,{})
        return render_to_response("admina/notaccess.html",c)


    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            AddReadAll(user_id)


    data = GetAccessAll()
    form = UserForm()
    c = RequestContext(request,{'data':data, 'form': form})
    c.update(csrf(request))
    return render_to_response("admina/readall.html",c)





### --- Интерфейс состава групп ---
def	Groups(request):




    ### --- Проверка доступа к этой закладки ---
    if AccessAdmin(request) != 'OK':
        c = RequestContext(request,{})
        return render_to_response("admina/notaccess.html",c)


    if request.method == 'POST':
        form = GroupsForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            group_id = form.cleaned_data['group']
            AddUserGroup(user_id, group_id)



    data = GetGroupsData()

    form = GroupsForm()
    c = RequestContext(request,{'data':data, 'form': form})
    c.update(csrf(request))
    return render_to_response("admina/groups.html",c)




## Удаление пользователя из доступа ко всем заявкам
def DelAccessAll(request):

    ### --- Проверка доступа к этой закладки ---
    if AccessAdmin(request) != 'OK':
        c = RequestContext(request,{})
        return render_to_response("admina/notaccess.html",c)

    user_id = request.GET['user_id']
    DelReadAll(user_id)


    return HttpResponseRedirect('/admina/readall')




## Удаление привязки пользователя к группе
def DelGroupData(request):

    ### --- Проверка доступа к этой закладки ---
    if AccessAdmin(request) != 'OK':
        c = RequestContext(request,{})
        return render_to_response("admina/notaccess.html",c)

    user_id = request.GET['user_id']
    group_id = request.GET['group_id']

    DelUserGroup(user_id,group_id)


    return HttpResponseRedirect('/admina/groups')

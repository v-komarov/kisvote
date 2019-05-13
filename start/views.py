#coding:utf-8
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	kis.lib.client	import	AuthUser
from	kis.lib.userdata	import	GetFio, GetPhone, GetEmail, GetUserKod, GetFirstName, GetLastName, GetSurName, GetJob
from	kis.lib.start		import	UserSave


def	Home(request):

    error = 'OK'

    ### --- Получение логина и пароля ---
    try:
        login = request.POST['login']
        password = request.POST['password']
        if login != '' and password != '':
            if AuthUser(login,password,request) == 'access accepted':
                c = RequestContext(request,{'fio':GetFio(request),'phone':GetPhone(request),'email':GetEmail(request)})
                c.update(csrf(request))
                UserSave(GetUserKod(request),GetLastName(request),GetFirstName(request),GetSurName(request),GetEmail(request),GetPhone(request),GetJob(request))
                return render_to_response("start/begin.html",c)
        else:
            error = 'Неправильные логин или пароль!'
    except:
        pass


    c = RequestContext(request,{'error':error})
    c.update(csrf(request))
    return render_to_response("start/start.html",c)



def	Exit(request):

    try:
        del request.session['key999']
    except:
        pass

    return HttpResponseRedirect('/')

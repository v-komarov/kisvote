#coding:utf-8
import	os.path
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod,GetEmail
from	forms			import	PersonForm
from	kis.lib.contract	import	GetDData,GetDPerson,CheckDAccess,AddDPerson,GetDPersonNext,DelDPerson
from	kis.lib.contract_mail	import	EmailToPerson,Remind







### --- Файлы ---
def	Page5(request):


    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')


    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
        return HttpResponseRedirect('/contract')



    if request.method == 'POST':
    	form = PersonForm(request.POST)
    	if form.is_valid():
    	    person = form.cleaned_data['person']
    	    r = AddDPerson(request,GetUserKod(request),contract_id,person)
    	    ### --- Уведомление согласующиму ---
    	    if r == 'OK':
    		EmailToPerson(contract_id)

    if request.method == 'GET':
    	try:
    	    delete_id = request.GET['delete_id']
    	    r = DelDPerson(request,GetUserKod(request),delete_id)
    	    ### --- Уведомление согласующиму ---
    	    if r == 'OK':
    		EmailToPerson(contract_id)
    	except:
    	    pass

	### --- Напоминание ---
	try:
	    remind = request.GET['remind']
	    email = request.GET['email']
	    Remind(email,remind,GetEmail(request))
	except:
	    pass


    ### --- Получение данных заявки ---
    data = GetDData(contract_id)

    form = PersonForm()
    #form.fields['status'].choices = status_list

    ### --- Получение истории статусов ---
    d = GetDPerson(contract_id)

    ### --- Получение следующего согласующего ---
    n = GetDPersonNext(contract_id)


    c = RequestContext(request,{'data':data,'form':form,'d':d,'n':n })
    c.update(csrf(request))
    return render_to_response("contract/page5.html",c)

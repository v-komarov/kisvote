#coding:utf-8
import	os.path
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	StatusForm
from	kis.lib.contract	import	GetDData,GetDStatusList,NewDStatus,GetDStatus,CheckDAccess
from	kis.lib.contract_mail	import	EmailStatusInfo,EmailToPerson,EmailComment






### --- Статус ---
def	Page4(request):



    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')


    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
        return HttpResponseRedirect('/contract')



    if request.method == 'POST':
    	form = StatusForm(request.POST)
    	if form.is_valid():
    	    comment = form.cleaned_data['comment']
    	    status = form.cleaned_data['status']
    	    r = NewDStatus(request,GetUserKod(request),contract_id,comment,status)
    	    if r == 'OK':
        		### --- Уведомление о статусе ---
                        EmailStatusInfo(contract_id)
        		### --- Уведомление согласующими ---
        		if status == '2' or status == '3':
        		    EmailToPerson(contract_id)
                        ### --- Уведомление о комментарии следующему согласующему ---
                        if status == '6':
                            EmailComment(contract_id)

    ### --- Получение данных заявки ---
    data = GetDData(contract_id)

    ### --- Доступные статусы ---
    status_list = GetDStatusList(data[5])
    form = StatusForm()
    form.fields['status'].choices = status_list

    ### --- Получение истории статусов ---
    d = GetDStatus(contract_id)

    c = RequestContext(request,{'data':data,'form':form,'d':d})
    c.update(csrf(request))
    return render_to_response("contract/page4.html",c)

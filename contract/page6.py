#coding:utf-8
import	os.path
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	EmailForm
from	kis.lib.contract	import	GetDData,CheckDAccess
from	kis.lib.contract_mail	import	Email2Ruk







### --- Email руководителю ---
def	Page6(request):



    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')


    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
	return HttpResponseRedirect('/contract')


    if request.method == 'POST':
    	form = EmailForm(request.POST)
    	if form.is_valid():
    	    email = form.cleaned_data['email']
    	    ### --- Доступно только для автора заявки ---
    	    if GetUserKod(request) == request.session['author_kod']:
    		Email2Ruk(email,contract_id)


    ### --- Получение данных заявки ---
    data = GetDData(contract_id)
    author_kod = data[9]
    request.session['author_kod'] = author_kod

    form = EmailForm()


    c = RequestContext(request,{'data':data,'form':form})
    c.update(csrf(request))
    return render_to_response("contract/page6.html",c)

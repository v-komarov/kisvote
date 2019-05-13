#coding:utf-8
import	os.path
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	kis.lib.contract	import	GetEmailHistory,GetDData,CheckDAccess







### --- История email уведомлений ---
def	Page7(request):


    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')

    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
	return HttpResponseRedirect('/contract')


    ### --- Получение номера страницы ---
    try:
        page = int(request.GET.get('page',1))
        request.session['page'] = page
    except:
        pass

    try:
        page = int(request.session['page'])
    except:
        page = 1



    ### --- Получение данных заявки ---
    data = GetDData(contract_id)


    d = GetEmailHistory(contract_id)

    paginator = Paginator(d,50)
    try:
        data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data_page = paginator.page(paginator.num_pages)


    c = RequestContext(request,{'data':data,'d':data_page})
    c.update(csrf(request))
    return render_to_response("contract/page7.html",c)

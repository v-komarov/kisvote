#coding:utf-8
import	os.path
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	LoadVer,LoadApp
from	kis.lib.contract	import	GetDData,LoadDVer,GetDVer,LoadDApp,GetDApp,CheckDAccess







### --- Версии договоров ---
def	Page2(request):


    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')


    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
        return HttpResponseRedirect('/contract')


    ### --- Отображение ---
    if request.method == 'GET':
    	try:
    	    doc_id = request.GET['doc_ver']
    	    f = GetDVer(doc_id)
    	    response = HttpResponse(content_type='application/%s' % f[0][-1:])
    	    attach = u'attachment; filename=\"%s\"' % (f[2])
    	    response['Content-Disposition'] = attach.encode('utf-8')
    	    response.write(f[1])
    	    return response
    	except:
    	    pass



    ### --- Отображение ---
    if request.method == 'GET':
    	try:
    	    doc_id = request.GET['doc_app']
    	    f = GetDApp(doc_id)
    	    response = HttpResponse(content_type='application/%s' % f[0][-1:])
    	    attach = u'attachment; filename=\"%s\"' % (f[2])
    	    response['Content-Disposition'] = attach.encode('utf-8')
    	    response.write(f[1])
    	    return response
    	except:
    	    pass





    if request.method == 'POST':
    	form = LoadVer(request.POST)
    	if form.is_valid():
    	    try:
        		load_ver_name = request.FILES['ver_load'].name
        		load_ver_data = request.FILES['ver_load'].read()
        		load_ver_name = load_ver_name.split('\\')[-1]
        		(path,ext) = os.path.splitext(load_ver_name)
        		load_ver_name = load_ver_name.replace(' ','_')
        		LoadDVer(request,GetUserKod(request),contract_id,load_ver_name,ext,load_ver_data)
    	    except:
        		pass


    if request.method == 'POST':
    	form2 = LoadApp(request.POST)
        if form2.is_valid():
            try:
                load_app_name = request.FILES['app_load'].name
                load_app_data = request.FILES['app_load'].read()
                load_app_name = load_app_name.split('\\')[-1]
                (path,ext) = os.path.splitext(load_app_name)
                load_app_name = load_app_name.replace(' ','_')
                LoadDApp(request,GetUserKod(request),contract_id,load_app_name,ext,load_app_data)
    	    except:
        		pass


    ### --- Получение данных заявки ---
    data = GetDData(contract_id)

    form = LoadVer()
    form2 = LoadApp()

    c = RequestContext(request,{'data':data,'form':form,'form2':form2})
    c.update(csrf(request))
    return render_to_response("contract/page2.html",c)

#coding:utf-8
import	os.path
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	LoadFile
from	kis.lib.contract	import	GetDData,AddDDocs,GetDDocsList,DelDDocs,GetDDocs,CheckDAccess







### --- Файлы ---
def	Page3(request):


    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')

    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
        return HttpResponseRedirect('/contract')



    ### --- Удаление приложенного документа ---
    if request.method == 'GET':
    	try:
    	    delete_id = request.GET['deletedoc']
    	    DelDDocs(delete_id)
    	except:
    	    pass

    ### --- Отображение файла ---
    if request.method == 'GET':
    	try:
    	    doc_id = request.GET['doc_id']
    	    f = GetDDocs(doc_id)
    	    response = HttpResponse(content_type='application/%s' % f[0][-1:])
    	    attach = u'attachment; filename=\"%s\"' % (f[2])
    	    response['Content-Disposition'] = attach.encode('utf-8')
    	    response.write(f[1])
    	    return response
    	except:
    	    pass


    if request.method == 'POST':
    	form = LoadFile(request.POST)
    	if form.is_valid():
    	    comment = form.cleaned_data['comment']
    	    load_file_name = request.FILES['file_load'].name
    	    load_file_data = request.FILES['file_load'].read()
    	    load_file_name = load_file_name.split('\\')[-1]
    	    (path,ext) = os.path.splitext(load_file_name)
    	    load_file_name = load_file_name.replace(' ','_')
    	    AddDDocs(GetUserKod(request),contract_id,load_file_name,comment,ext,load_file_data)
    form = LoadFile()

    ### --- Получение данных заявки ---
    data = GetDData(contract_id)

    ### --- Получение списка документов ---
    d = GetDDocsList(contract_id)

    c = RequestContext(request,{'data':data,'form':form,'d':d})
    c.update(csrf(request))
    return render_to_response("contract/page3.html",c)

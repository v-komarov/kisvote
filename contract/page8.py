#coding:utf-8
import	os.path
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	cStringIO	import	StringIO

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	PersonForm
from	kis.lib.contract	import	GetDData,GetDPerson,CheckDAccess, Name_Boss
from	kis.lib.contract_print	import	Stamp, Stamp2






### --- Штамп согласования ---
def	Page8(request):


    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')


    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
	return HttpResponseRedirect('/contract')


    ### --- Проверка доступа к этой закладки ---
    #if CheckAccess(request,'4') != 'OK':
    #	c = RequestContext(request,{})
    #	return render_to_response("contract/page8notaccess.html",c)



    ### --- Получение данных заявки ---
    data = GetDData(contract_id)

    ### --- Получение списка согласующих ---
    d = GetDPerson(contract_id)


    ### --- Имя руковдителя Руководителя ---
    boss = Name_Boss(contract_id)

    ### --- Получение списка отмеченных ---
    if request.method == 'POST':
    	person_kod = ["\"{}\"".format(data[9]),]
        for item in d:
            try:
                p_kod = request.POST[item[14]]
                if p_kod == 'on':
                    person_kod.append("\"{}\"".format(item[14].encode('utf-8')))
            except:
                pass
    	
        response = HttpResponse(Stamp2(contract_id,person_kod), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = u'attachment; filename="stamp_%s.docx"' % contract_id
        return response

    	"""
    	response = HttpResponse(content_type='application/pdf')
    	response['Content-Disposition'] = 'attachment; filename="stamp.pdf"'
    	buff = StringIO()
    	result = Stamp(buff,contract_id,person_kod)
    	response.write(result.getvalue())
    	buff.close()
    	return response
    	"""


    c = RequestContext(request,{'data':data,'d':d, 'boss':boss})
    c.update(csrf(request))
    return render_to_response("contract/page8.html",c)

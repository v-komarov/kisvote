#coding:utf-8
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	FilterForm,ContractForm,EmailAuthorForm,EmailGroupForm
from	kis.lib.contract	import	GetDList,GetDData,NewD,EditD,CheckDAccess,GetAuthorEmail,SaveAuthorEmail,AddGroupEmail,GetGroupEmail,DelGroupEmail,GetToVoteList





### --- Список ---
def	List(request):


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




    if request.method == 'POST':

        form = FilterForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            status = form.cleaned_data['status']
            request.session['search'] = search
            request.session['status'] = status
    else:
        form = FilterForm()

    try:
        search = request.session['search']
        status = request.session['status']
    except:
        search = ''
        status = 'ACTIVE'


    form.fields['search'].initial = search
    if search !='' :
        form.fields['status'].initial = 'ALL'
#	form.fields['status'].widget.attrs['disabled'] = True
    else:
        form.fields['status'].initial = status

    data = GetDList(search,status)

    paginator = Paginator(data,50)
    try:
        data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data_page = paginator.page(paginator.num_pages)



    c = RequestContext(request,{'data':data_page,'form':form})
    c.update(csrf(request))
    return render_to_response("contract/list.html",c)






### --- Список заявок на согласование ---
def	ToVote(request):

    data = GetToVoteList(GetUserKod(request))

    c = RequestContext(request,{'data':data})
    c.update(csrf(request))
    return render_to_response("contract/tovote.html",c)






### --- Редактирование заявки ---
def	EditPage1(request):


    ### --- Кода заявки  ---
    try:
        contract_id = request.GET['contract_id']
        request.session['contract_id'] = contract_id
    except:
        pass
    try:
        contract_id = request.session['contract_id']
    except:
        return HttpResponseRedirect('/contract')


    ### --- Проверка доступа именно к этой заявке ---
    if CheckAccess(request) != 'OK':
        return HttpResponseRedirect('/contract')



    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contragent = form.cleaned_data['contragent']
            tema = form.cleaned_data['tema']
            text = form.cleaned_data['text']
            result = EditD(contract_id,contragent,tema,text)
            if result == 'OK':
                return HttpResponseRedirect('/page3contract')


    ### --- Получение данных заявки ---
    data = GetDData(contract_id)
    form = ContractForm()

    form.fields['contragent'].initial = data[3]
    form.fields['tema'].initial = data[4]
    form.fields['text'].initial = data[8]
    if data[5] != '0':
        form.fields['contragent'].widget.attrs['readonly'] = True
        form.fields['tema'].widget.attrs['readonly'] = True
        form.fields['text'].widget.attrs['readonly'] = True

    c = RequestContext(request,{'data':data,'form':form})
    c.update(csrf(request))
    return render_to_response("contract/edit.html",c)








### --- Добавление новой заявки ---
def	New(request):


    if request.method == 'POST':

        form = ContractForm(request.POST)
        if form.is_valid():
            contragent = form.cleaned_data['contragent']
            tema = form.cleaned_data['tema']
            text = form.cleaned_data['text']
            result = NewD(GetUserKod(request),contragent,tema,text)
            if result != 'ERRORDATA':
                return HttpResponseRedirect("/editcontract/?contract_id=%s" % result)


    form = ContractForm()

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("contract/new.html",c)





### --- Группы рассылки email ---
def	Opt(request):

    ### --- Проверка доступа к настройкам ---
    #if CheckAccess(request,'4') != 'OK':
	#return render_to_response("contract/optnotaccess.html")

    if request.method == 'POST':
    	f1 = EmailGroupForm(request.POST)
    	f2 = EmailAuthorForm(request.POST)
    	if f2.is_valid():
    	    email = f2.cleaned_data['authoremail']
    	    SaveAuthorEmail(email)
    	if f1.is_valid():
    	    email = f1.cleaned_data['groupemail']
    	    AddGroupEmail(email)

    if request.method == 'GET':
	try:
	    delete_id = request.GET['delete_gemail']
	    DelGroupEmail(delete_id)
	except:
	    pass

    data = GetGroupEmail()

    f1 = EmailGroupForm()
    f2 = EmailAuthorForm()
    f2.fields['authoremail'].initial = GetAuthorEmail()

    c = RequestContext(request,{'f1':f1,'f2':f2,'data':data})
    c.update(csrf(request))
    return render_to_response("contract/opt.html",c)

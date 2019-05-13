#coding:utf-8
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	DateFilterForm
from	kis.lib.contract	import	GetPersonResult





### --- Отчет по согласователям ---
def	PersonResult(request):



    if request.method == 'POST':

        form = DateFilterForm(request.POST)
        if form.is_valid():
            date1 = form.cleaned_data['date1']
            date2 = form.cleaned_data['date2']
            request.session['date1'] = date1
            request.session['date2'] = date2
    else:
        form = DateFilterForm()

    try:
        date1 = request.session['date1']
        date2 = request.session['date2']
    except:
        date1 = ''
        date2 = ''


    form.fields['date1'].initial = date1
    form.fields['date2'].initial = date2
    
    if date1 != '' and date2 != '':
        data = GetPersonResult(date1,date2)
    else:
        data = []


    c = RequestContext(request,{'form':form, 'data':data, 'n':0})
    c.update(csrf(request))
    return render_to_response("contract/personresult.html",c)



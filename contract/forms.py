#coding:utf-8

from	django	import	forms

from	kis.lib.contract	import	GetStatusList,GetStatusListAll,GetDPersonList,GetEmailRukList


class	FilterForm(forms.Form):
    search = forms.CharField(label='Строка поиска',required=False)
    status = forms.ChoiceField(label='Статус',choices=GetStatusList())


class	DateFilterForm(forms.Form):
    date1 = forms.CharField(label='с',required=False)
    date2 = forms.CharField(label='по',required=False)



class	ContractForm(forms.Form):
    contragent = forms.CharField(label='Контрагент*',widget=forms.TextInput(attrs={'class':'g-5',}))
    tema = forms.CharField(label='Тема*',widget=forms.TextInput(attrs={'class':'g-5',}))
    text = forms.CharField(label='Текст заявки',widget=forms.Textarea(attrs={'class':'g-5',}),required=False)



class	LoadFile(forms.Form):
    comment = forms.CharField(label='Описание документа (файла)*',widget=forms.Textarea)
    file_load = forms.FileField(label='Файл*',widget=forms.FileInput,required=False)



class	StatusForm(forms.Form):
    comment = forms.CharField(label='Комментарий',required=False,widget=forms.Textarea)
    status = forms.ChoiceField(label='Статус',required=False,choices=GetStatusListAll())


### --- Загрузка версии договора ---
class	LoadVer(forms.Form):
    ver_load = forms.FileField(label='Файл договора*',widget=forms.FileInput,required=False)


### --- Загрузка приложения ---
class	LoadApp(forms.Form):
    app_load = forms.FileField(label='Файл приложения*',widget=forms.FileInput,required=False)


### --- Форма добавления согласующего ---
class	PersonForm(forms.Form):
    person = forms.ChoiceField(label='Выбор согласующего',required=False,choices=[])
    def	__init__(self,*args,**kwargs):
	super(PersonForm,self).__init__(*args,**kwargs)
	self.fields['person'].choices = GetDPersonList()


### --- Форма отправки email руководителю ---
class	EmailForm(forms.Form):
    email = forms.ChoiceField(label='Выбор получателя сообщения',required=False,choices=GetEmailRukList())
    def	__init__(self,*args,**kwargs):
	super(EmailForm,self).__init__(*args,**kwargs)
	self.fields['email'].choices = GetEmailRukList()


### --- Email обратного адреса ---
class	EmailAuthorForm(forms.Form):
    authoremail = forms.EmailField(label='Обратный адрес')


### --- Ввод адреса рассылки ---
class	EmailGroupForm(forms.Form):
    groupemail = forms.EmailField(label='Адрес рассылки')

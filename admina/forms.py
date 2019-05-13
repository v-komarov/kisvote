#coding:utf-8

from django import forms


from	kis.lib.contract	import	GetDPersonList
from kis.lib.admina import GetGroupsList



class	UserForm(forms.Form):
    user = forms.ChoiceField(label='Выбор пользователя',required=False,choices=[])
    def	__init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields['user'].choices = GetDPersonList()




class	GroupsForm(forms.Form):
    user = forms.ChoiceField(label='Выбор пользователя',required=False,choices=[])
    group = forms.ChoiceField(label='Группа',required=False,choices=[])
    def	__init__(self,*args,**kwargs):
        super(GroupsForm,self).__init__(*args,**kwargs)
        self.fields['user'].choices = GetDPersonList()
        self.fields['group'].choices = GetGroupsList()

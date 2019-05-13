#coding:utf-8


from kis.lib.contract import ChAccess



def	GetFio(request):
    return u"{} {} {}".format(request.session['key999']['lastname'],request.session['key999']['firstname'],request.session['key999']['surname'])


def	GetPhone(request):
    return u"{}".format(request.session['key999']['phone'])


def	GetEmail(request):
    return u"{}".format(request.session['key999']['email'])


def	GetUserKod(request):
    return u"{}".format(request.session['key999']['id'])


def GetFirstName(request):
    return u"{}".format(request.session['key999']['firstname'])


def GetSurName(request):
    return u"{}".format(request.session['key999']['surname'])


def GetLastName(request):
    return u"{}".format(request.session['key999']['lastname'])


def GetJob(request):
    return u"{}".format(request.session['key999']['job'])


def GetContractId(request):
    return u"{}".format(request.session['contract_id'])






def	CheckAccess(request):

    user_id = GetUserKod(request)
    contract_id = GetContractId(request)
    return ChAccess(contract_id,user_id)



## -- Принадлежность к группе администрирования
def AccessAdmin(request):

    if 'matchadmin' in request.session['key999']['groups']:
        return "OK"
    else:
        return "error"

    """
    if group in request.session['key888']['groups']:
        return 'OK'
    else:
        return 'NOTACCESS'
    """
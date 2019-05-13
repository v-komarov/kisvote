#coding:utf-8

from	django.db		import	connections, transaction
from	django.core.mail	import	send_mail
from	kis.lib.contract	import	GetDData,WriteEmailRuk,EmailHistory,GetGroupEmail,GetAuthorEmail,GetDPersonNextEmail,PersonEmailOk,PersonLagDays,GetDStatus
from	kis.lib.contract	import	GetDPersonNextList, GetDPersonNext
from django.core.mail import EmailMessage



kisip = "http://10.6.3.54:8040"




### --- Список адресов группы рассылки ---
def	Emails():
    mail_list = GetGroupEmail()
    m = []
    for item in mail_list:
        m.append(item[0])

    return m



### --- Отправка запроса подписи ---
def	Email2Ruk(email,contract_id):

    data = GetDData(contract_id)

    address = []
    address.append(email)
    m = u"""
    <p>
    Прошу подписать заявку № {contract} (Заявки договоры) <a href="{kisip}/editcontract/?contract_id={contract}">Ссылка</a><br>
    Контрагент: {contragent}<br>
    Тема: {tema}<br>
    Содержание заявки:<br>
    {task}<br>
    </p>
    """.format(contract=data[0],kisip=kisip,contragent=data[3],tema=data[4],task=data[8])

    subj = 'KIS-messager D '+data[0]

    m = EmailMessage(
        subject = subj,
        body = m,
        from_email = data[14],
        to = address
    )

    m.content_subtype = "html"
    m.send()

    #send_mail('KIS-messager D '+data[0],m,data[14],address)

    ### --- Фиксируем email в заявке ---
    WriteEmailRuk(contract_id,email)
    ### -- Собираем отправку в лог ---
    EmailHistory(contract_id,email,u'Запрос на подпись заявки')





### --- Рассылка коментария следующему согласующемо , если заявка в процессе согласования
def EmailComment(contract_id):
    ### --- Получение данных по заявке ---
    d = GetDData(contract_id)

    ### --- Получение последней записи из истории статусов ---
    last_status = GetDStatus(contract_id)[0]


    ### --- Для статусов Договор не согласован  ---
    if d[5] == '3':

        author = last_status[10]
        ### --- Добавление адреса автора комментария
        mail = []
        
        ### -- Добавление email адреса инициатора заявки , если нет
        #if not d[14] in mail: 
        #    mail.append(d[14])

        ### -- Добавление адреса следующего согласующего
        next_p = GetDPersonNext(contract_id)
        if len(next_p) == 3:
            if not next_p[2] in mail:
                mail.append(next_p[2])


        for address in mail:

            m = u"""<p>
            Модуль согласования документов<br><br>
            Уведомление о коментарии заявки № {contract} <a href="{kisip}/editcontract/?contract_id={contract}">Ссылка</a><br>
            Контрагент: {contragent}<br>
            Тема: {tema}<br><br>
            Коментарий: {message}<br>
            Автор: {name1} {name2}
            </p>
            """.format(contract=d[0],kisip=kisip,contragent=d[3],tema=d[4],message=last_status[2],name1=last_status[7],name2=last_status[6])

            subj = 'KIS-messager D '+d[0]

            em = EmailMessage(
                subject = subj,
                body = m,
                from_email = author,
                to = [address,]
            )

            em.content_subtype = "html"
            em.send()


            EmailHistory(contract_id,address,u'Уведомление о коментарии')





#### --- Рассылка уведомлений по статусу заявки ---
def	EmailStatusInfo(contract_id):
    ### --- Получение данных по заявке ---
    d = GetDData(contract_id)

    ### --- Получение последнего установленного статуса из истории статусов ---
    last_status = GetDStatus(contract_id)[0]

    ### --- Для статусов Комментарий и Договор не согласован рассылку не делаем ---
    #if d[5] != '3' and d[5] != '6':

    mail = Emails()
    mail.append(d[14])
    author = "Согласование документов <{}>".format(GetAuthorEmail())

    ### --- уточнение статуса заявки для процесса согласования ---

    ### --- Если документ согласован - то оповещение по дополнительным email адресам.
    if d[5] == '2':
        mail.append('m.lopatina@sibir.ttk.ru')
        mail.append('office@sibir.ttk.ru')

    for address in mail:

        m = u"""<p>
        Модуль согласования документов<br><br>
        Уведомление о статусе заявки № {contract} <a href="{kisip}/editcontract/?contract_id={contract}">Ссылка</a><br>
        Контрагент: {contragent}<br>
        Тема: {tema}<br><br>
        Статус: {status}<br>
        Сообщение: {message}<br>
        Автор: {name1} {name2}
        </p>
        """.format(contract=d[0],kisip=kisip,contragent=d[3],tema=d[4],status=last_status[3],message=last_status[2],name1=last_status[7],name2=last_status[6])

        subj = 'KIS-messager D '+d[0]

        em = EmailMessage(
            subject = subj,
            body = m,
            from_email = author,
            to = [address,]
        )

        em.content_subtype = "html"
        em.send()


        EmailHistory(contract_id,address,u'Уведомление о статусе: '+last_status[3])





### --- Приглашение к согласованию версии договора ---
def	EmailToPerson(contract_id):

    ### --- Получение данных по заявке ---
    d = GetDData(contract_id)
    author = "Согласование документов <{}>".format(GetAuthorEmail())

    ### --- Определение следующего согласующего ---
    try:
        (person_kod,email,send) = GetDPersonNextEmail(contract_id)
    except:
        (person_kod,email,send) = ['','','']
    ### --- Проверка : отправлялось ли уже сообщение этому согласующему ---
    if send == 'NO':
        m = u"""
        <p>
        Модуль согласования документов<br><br>
        Уведомление о необходимости согласования заявки № {contract} <a href="{kisip}/editcontract/?contract_id={contract}">Ссылка</a><br>
        Контрагент: {contragent}<br>
        Тема: {tema}<br><br>
        Предлагаем согласовать версию договора.
        </p>
        """.format(contract=d[0],kisip=kisip,contragent=d[3],tema=d[4])

        subj = 'KIS-messager D '+d[0]

        em = EmailMessage(
            subject = subj,
            body = m,
            from_email = author,
            to = [email,]
        )

        em.content_subtype = "html"
        em.send()


	EmailHistory(contract_id,email,u'Уведомление согласующему.')

	### --- Отметка, что email согласующему отправлен ---
	PersonEmailOk(contract_id,person_kod)




#### --- Напоминатель согласователю из интерфейса ---
def	Remind(mail,d_id,author):

    d = GetDData(d_id)

    m = u"""
    <p>
    Модуль согласования документов<br><br>
    Напоминание о необходимости согласования заявки № {contract} <a href="{kisip}/editcontract/?contract_id={contract}">Ссылка</a><br>
    Контрагент: {contragent}<br>
    Тема: {tema}<br><br>
    Предлагаем согласовать версию договора.
    </p>
    """.format(contract=d_id,kisip=kisip,contragent=d[3],tema=d[4])

    subj = 'KIS-messager D '+d[0]

    em = EmailMessage(
        subject = subj,
        body = m,
        from_email = author,
        to = [mail,]
    )

    em.content_subtype = "html"
    em.send()


    EmailHistory(d_id,mail,u'Напоминание согласующему.')







#### --- Напоминатель согласователям ---
def	Remember(days=3):
    data = PersonLagDays(days)
    author = GetAuthorEmail()
    for item in data:
	day_str = "%s" % item[0]
	d = GetDData(day_str)
	email = item[6]

	m = u"""
	<p>
	Модуль согласования документов<br><br>
	Напоминание о необходимости согласования заявки № {contract} <a href="{kisip}/editcontract/?contract_id={contract}">Ссылка</a><br>
	Контрагент: {contragent}<br>
	Тема: {tema}<br><br>
	Предлагаем согласовать версию договора.
	</p>
	""".format(contract=d[0],kisip=kisip,contragent=d[3],tema=d[4])
	#send_mail('KIS-messager D '+d[0],m,author,[email,])

	subj = 'KIS-messager D '+d[0]

	em = EmailMessage(
	    subject = subj,
	    body = m,
	    from_email = author,
            to = [email,]
        )

        em.content_subtype = "html"
        em.send()


        EmailHistory(d[0],email,u'Напоминание согласующему.')



### --- Отправка каждому следующему согласующему список договоров ---
def	PersonNextList():
    nextpersons = {}
    for pe in GetDPersonNextList():
        if nextpersons.has_key(pe[2]):
            kod_d = pe[3]
            email = pe[2]
            nextpersons[email].append(kod_d)
        else:
            nextpersons[pe[2]] = [pe[3]]

        for email in nextpersons.keys():

            m = u"""
            <p>
            Модуль согласования документов<br><br>
            Напоминание о необходимости согласования следующих заявок:<br>
            </p>
            """

            ### --- Информация по каждому договору
            for kod in nextpersons[email]:
                dogdata = GetDData(kod)
                m2 = u"""
                <p>
                Номер заявки: {contract} <a href="{kisip}/editcontract/?contract_id={contract}">Ссылка</a><br>
                Контрагент: {contragent}<br>
                Тема: {tema}<br>
                </p>
                """.format(contract=kod,kisip=kisip,contragent=dogdata[3],tema=dogdata[4])
                m = m + m2

            subj = 'KIS-messager ALL REQUEST'

            em = EmailMessage(
                subject = subj,
                body = m,
                from_email = "Согласование документов <{}>".format('uo@sibir.ttk.ru'),
                to = [email,'v.komarov@sibir.ttk.ru']
            )

            em.content_subtype = "html"
            em.send()

#coding:utf-8

import datetime
from	django.db	import	connections
import	psycopg2




### Список с доступом ко всем заявкам
def	GetAccessAll():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_d_readall;")
    data = cursor.fetchall()

    return data




### Список распределения по группам
def	GetGroupsData():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_d_persons_groups;")
    data = cursor.fetchall()

    return data




### Список групп
def	GetGroupsList():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_rec_id,t_user_name2||' '||t_user_name1 FROM t_user_kis WHERE t_user_name3='_' ORDER BY t_user_name1;")
    data = cursor.fetchall()

    return data



### Удаление прав ко всем заявкам
def DelReadAll(user_id):
    cursor = connections['main'].cursor()
    cursor.execute("DELETE FROM t_d_access WHERE t_user_id=%s;", (user_id,))
    return "OK"



### Удаление пользователя из группы
def DelUserGroup(user_id,group_id):
    cursor = connections['main'].cursor()
    cursor.execute("DELETE FROM t_d_persons_groups WHERE user_id=%s AND group_id=%s;", (user_id,group_id))
    return "OK"



### Добавление пользователю прав доступа ко всем заявкам
def AddReadAll(user_id):
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_adddreadall(%s);", (user_id,))
    return "OK"



### Добавление пользователя к группу
def AddUserGroup(user_id,group_id):
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_adddgroup(%s,%s);", (user_id,group_id))
    return "OK"



### Изменение инициатора заявки
def ChAuthor(d,author_after,user_id):
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_d_chauthor(%s,%s,%s);", (d,author_after,user_id))
    return "OK"


### История изменений инициаторов заявок
def GetChAuthor():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_d_show_changing_author;")
    data = cursor.fetchall()
    return data

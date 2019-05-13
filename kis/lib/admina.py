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

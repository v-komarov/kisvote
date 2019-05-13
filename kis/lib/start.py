#coding:utf-8

from	django.db	import	connections




def	UserSave(user_kod,name1,name2,name3,email,phone,job):
    user_kod = user_kod.encode("utf-8")
    name1 = name1.encode("utf-8")
    name2 = name2.encode("utf-8")
    name3 = name3.encode("utf-8")
    email = email.encode("utf-8")
    phone = phone.encode("utf-8")
    job = job.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_UserSave2(%s,%s,%s,%s,%s,%s,%s);", [user_kod,name1,name2,name3,email,phone,job])
    data = cursor.fetchone()
    cursor.close()
    return data


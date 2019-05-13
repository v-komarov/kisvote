#coding:utf-8

import	json
import	urllib2





### --- Данные заявки в формате json ---
class	JsonUser():

    def	__init__(self,user_id):

	self.url = "http://10.6.1.28/userdataservice/?user_id=%s" % user_id
	self.json_str = urllib2.urlopen(self.url).read()
	self.json_str = self.json_str.encode("utf-8")

	self.j = json.loads(self.json_str)


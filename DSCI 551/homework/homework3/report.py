import sys
import mysql.connector
import json


date, outfile_name = sys.argv[1],sys.argv[2]

class App(dict):
	def __str__(self):
		return json.dumps(self)

fp =open(outfile_name, 'w')
date = date.split('/');
date = date[1] + "-" + date[0] + "%";

cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', host = '127.0.0.1', database = 'covid19')
cursor = cnx.cursor()

query = "select sex, sum(confirmed), sum(deceased) from timegender where date like '%s' group by sex" % date

query1 = "select age, sum(confirmed), sum(deceased) from timeage where date like '%s' group by age"% date

query2 = "select province, sum(confirmed), sum(deceased) from timeprovince where date like '%s' group by province" % date

ret = []

cursor.execute(query)

gender_list = []
for item in cursor:
	dict_gender = {}
	dict_gender["confirmed"] = int(item[1])
	dict_gender["deceased"] = int(item[2])
	gender_list.append([item[0], dict_gender])

gender = App(gender_list)
ret.append(["gender", gender])

cursor.execute(query1)

age_list = []
for item in cursor:
	dict_age = {}
	dict_age["confirmed"] = int(item[1])
	dict_age["deceased"] = int(item[2])
	age_list.append([item[0], dict_gender])
age = App(age_list)
ret.append(["age", age])

cursor.execute(query2)

province_list = []
for item in cursor:
	dict_province = {}
	dict_province["confirmed"] = int(item[1])
	dict_province["deceased"] = int(item[2])
	province_list.append([item[0], dict_province])
province = App(province_list)
ret.append(["province", province])

pairs = App(ret)
json.dump(pairs,fp)


fp.close()
cursor.close()
cnx.close()

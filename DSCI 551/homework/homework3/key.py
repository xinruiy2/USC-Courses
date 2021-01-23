import sys
import mysql.connector


table_name, attributes = sys.argv[1], sys.argv[2]

attributes = attributes.split(',')
attribute = ""
for attr in attributes:
	attribute += attr + ","
attribute = attribute[:-1]


cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', host = '127.0.0.1', database = 'covid19')
cursor = cnx.cursor()

query = "select %s, count(*) from `%s` group by %s having count(*) > 1 order by count(*) DESC limit 5" % (attribute, table_name, attribute) 

#select age, confirmed, count(*) from timeage group by age, confirmed having count(*) > 1 order by count(*) DESC limit 5

cursor.execute(query)

ifContain = 0
for item in cursor:
	ifContain = 1
	s = ""
	for i in item:
		s += str(i) + ","
	print(s[:-1])
		
if ifContain == 0:
	print("yes")



cursor.close()
cnx.close()

import sys
import mysql.connector

initial_id = sys.argv[1]

cnx = mysql.connector.connect(user = 'dsci551', password = 'dsci551', host = '127.0.0.1', database = 'covid19')
cursor = cnx.cursor()

dict_id = {}
list = []

curr_id = initial_id
ifEndByNull = 0

while(curr_id not in dict_id):
    dict_id[curr_id] = len(list)
    list.append(curr_id)
    query = "select infected_by from patientinfo where patient_id = '%s'" % curr_id
    cursor.execute(query)
    ifEndByNull = 0
    for item in cursor:
        ifEndByNull = 1
        curr_id = item[0]
        if curr_id in dict_id:
            break
    if ifEndByNull == 0:
        break

if ifEndByNull == 0:
    ret = ""
    for n in list:
        ret += str(n) + ","
    print(ret[:-1])
else:
    ret = "Cycle found: "
    for i in range(dict_id[curr_id], len(list)):
        ret += str(list[i]) + ","
    ret += str(curr_id)
    print(ret)

cursor.close()
cnx.close()

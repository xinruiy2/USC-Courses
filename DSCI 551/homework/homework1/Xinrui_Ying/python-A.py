import json
import sys

country_json = sys.argv[1]
city_json = sys.argv[2]
country_language_json = sys.argv[3]

f = open(country_json,)
data = json.load(f)
country_name = []
capital_id = {}
count = 0

for d in data:
    if d["Continent"] == "North America":
        country_name.append(d["Name"])
        capital_id[d["Capital"]] = count
        count += 1

f.close()
capital_name = ["" for i in range(len(country_name))]

f = open(city_json,)
data = json.load(f)

for d in data:
    if d["ID"] in capital_id:
        capital_name[capital_id[d['ID']]] = d["Name"]

for i in range(len(capital_name)):
    print(country_name[i] + ",   " + capital_name[i])
f.close()

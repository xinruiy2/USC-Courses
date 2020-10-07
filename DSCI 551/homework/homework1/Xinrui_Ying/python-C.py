import json
import sys

country_json = sys.argv[1]
city_json = sys.argv[2]
country_language_json = sys.argv[3]

f = open(country_json,)
data = json.load(f)

total_number_LifeExpectancy = {}
total_number_Country = {}
number_of_GNP = {}

for d in data:
    if d["Continent"] in total_number_LifeExpectancy:
        total_number_LifeExpectancy[d["Continent"]] += d["LifeExpectancy"]
        total_number_Country[d["Continent"]] += 1
        if d["GNP"] > 10000:
            number_of_GNP[d["Continent"]] += 1
    else:
        total_number_LifeExpectancy[d["Continent"]] = d["LifeExpectancy"]
        total_number_Country[d["Continent"]] = 1
        if d["GNP"] > 10000:
            number_of_GNP[d["Continent"]] = 1
        else:
            number_of_GNP[d["Continent"]] = 0

for n in total_number_Country.keys():
    if number_of_GNP[n] >= 5:
        print(n + "  " + str(float(total_number_LifeExpectancy[n])/total_number_Country[n]))

f.close()

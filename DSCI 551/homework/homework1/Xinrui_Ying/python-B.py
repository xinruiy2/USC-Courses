import json
import sys

country_json = sys.argv[1]
city_json = sys.argv[2]
country_language_json = sys.argv[3]

f = open(country_json,)
data = json.load(f)

country_code = {}

for d in data:
    if d["Continent"] == "North America":
        country_code[d["Code"]] = d["Name"]


f = open(country_language_json,)
data = json.load(f)

language_dict = {}

for d in data:
    if d["CountryCode"] in country_code and d["IsOfficial"] == "T":
        if d["CountryCode"] in language_dict:
            language_dict[d["CountryCode"]] += ", " + d["Language"]
        else:
            language_dict[d["CountryCode"]] = d["Language"]

for key in country_code.keys():
    if key in language_dict:
        print(country_code[key] + ", " + language_dict[key])
    else:
        print(country_code[key] + ", " + "None")
# should have 37 countries
f.close()

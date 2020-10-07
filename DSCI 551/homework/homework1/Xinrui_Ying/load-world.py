import requests
import json
import sys

country_json = sys.argv[1]
city_json = sys.argv[2]
country_language_json = sys.argv[3]

class App(dict):
    def __str__(self):
        return json.dumps(self)

# city.json
url = "https://world-abe82.firebaseio.com/world/city.json"
f = open(city_json,)
data = json.load(f)

city_list = []
for d in data:
    id = d["ID"]
    del d["ID"]
    city_list.append([id, d])
pairs = App(city_list)

fp =  open('temp.json', 'w')
json.dump(pairs, fp)
fp = open('temp.json', 'r')
response = requests.put(url, fp)
f.close()
fp.close()

# country.json
url = "https://world-abe82.firebaseio.com/world/country.json"
f = open(country_json,)
data = json.load(f)

country_list = []
for d in data:
    id = d["Code"]
    del d["Code"]
    country_list.append([id, d])
pairs = App(country_list)

fp =  open('temp.json', 'w')
json.dump(pairs, fp)
fp = open('temp.json', 'r')
response = requests.put(url, fp)
f.close()
fp.close()

# countrylanguage.json
url = "https://world-abe82.firebaseio.com/world/countrylanguage.json"
f = open(country_language_json,)
data = json.load(f)

dict_countryToLanguage = {}

for d in data:
    id = d["CountryCode"]
    language = d["Language"]
    if(language == "[South]Mande"):
        language = "Mande"
    del d["CountryCode"]
    del d["Language"]
    if id in dict_countryToLanguage:
        dict_countryToLanguage[id][0].update(App([[language,d]]))
    else:
        dict_countryToLanguage[id] = [App([[language,d]])]

country_language = []
for key in dict_countryToLanguage.keys():
    country_language.append([key, dict_countryToLanguage[key][0]])
pairs = App(country_language)
fp =  open('temp.json', 'w')
json.dump(pairs, fp)
fp = open('temp.json', 'r')
response = requests.put(url, fp)
f.close()
fp.close()

#country nested
url = "https://world-abe82.firebaseio.com/world/country_nested.json"
for country in country_list:
    if country[0] in dict_countryToLanguage:
        country[1].update(App([["language",dict_countryToLanguage[country[0]][0]]]))

pairs = App(country_list)
fp =  open('temp.json', 'w')
json.dump(pairs, fp)
fp = open('temp.json', 'r')
response = requests.put(url, fp)
f.close()
fp.close()

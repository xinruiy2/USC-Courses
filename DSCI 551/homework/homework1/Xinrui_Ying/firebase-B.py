import requests

url = 'https://world-abe82.firebaseio.com/world/country.json?orderBy=%22Continent%22&equalTo=%22North%20America%22&print=pretty'
country_data = requests.get(url).json()
# print(len(requests.get(url).text))

# count = 0
for key in country_data.keys():
    of_language = ""
    url = "https://world-abe82.firebaseio.com/world/countrylanguage.json?orderBy=%22$key%22&equalTo=%22" + key + "%22"
    countrylanguage_data = requests.get(url).json()
    # count += len(requests.get(url).text)
    for sm_key in countrylanguage_data[key].keys():
        if countrylanguage_data[key][sm_key]["IsOfficial"] == "T":
            of_language += sm_key + ", "
    if of_language == "":
        of_language = "None"
    else:
        of_language = of_language[:-2]
    print(country_data[key]["Name"] + ",   " + of_language)
# print(count)

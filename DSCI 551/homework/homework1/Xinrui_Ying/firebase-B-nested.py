import requests

url = "https://world-abe82.firebaseio.com/world/country_nested.json?orderBy=%22Continent%22&equalTo=%22North%20America%22&print=pretty"
country_nested_data = requests.get(url).json()
# print(len(requests.get(url).text))
for key in country_nested_data.keys():
    of_language = ""
    for sm_key in country_nested_data[key]["language"].keys():
        if country_nested_data[key]["language"][sm_key]["IsOfficial"] == "T":
            of_language += sm_key + ", "
    if of_language == "":
        of_language = "None"
    else:
        of_language = of_language[:-2]
    print(country_nested_data[key]["Name"] + ",   " + of_language)

import requests

url = 'https://world-abe82.firebaseio.com/world/country.json?orderBy=%22Continent%22&equalTo=%22North%20America%22&print=pretty'
country_data = requests.get(url).json()
# print(len(requests.get(url).text))

# count = 0
for key in country_data.keys():
    capital_id = country_data[key]["Capital"]
    url = "https://world-abe82.firebaseio.com/world/city.json?orderBy=%22$key%22&equalTo=%22"+ str(capital_id) + "%22"
    city_data = requests.get(url).json()
    # count += len(requests.get(url).text)
    print(country_data[key]["Name"] + ",   " + city_data[str(capital_id)]["Name"])
# print(count)

import requests

url = "https://world-abe82.firebaseio.com/world/country.json"
country_data = requests.get(url)
# print(len(requests.get(url).text))

total_number_LifeExpectancy = {}
total_number_Country = {}
number_of_GNP = {}

for key in country_data.json().keys():
    if country_data.json()[key]["Continent"] in total_number_LifeExpectancy:
        total_number_LifeExpectancy[country_data.json()[key]["Continent"]] += country_data.json()[key]["LifeExpectancy"]
        total_number_Country[country_data.json()[key]["Continent"]] += 1
        if country_data.json()[key]["GNP"] > 10000:
            number_of_GNP[country_data.json()[key]["Continent"]] += 1
    else:
        total_number_LifeExpectancy[country_data.json()[key]["Continent"]] = country_data.json()[key]["LifeExpectancy"]
        total_number_Country[country_data.json()[key]["Continent"]] = 1
        if country_data.json()[key]["GNP"] > 10000:
            number_of_GNP[country_data.json()[key]["Continent"]] = 1
        else:
            number_of_GNP[country_data.json()[key]["Continent"]] = 0

for n in total_number_Country.keys():
    if number_of_GNP[n] >= 5:
        print(n + "  " + str(float(total_number_LifeExpectancy[n])/total_number_Country[n]))

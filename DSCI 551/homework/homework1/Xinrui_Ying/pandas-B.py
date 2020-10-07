import pandas as pd
import sys

country_json = sys.argv[1]
city_json = sys.argv[2]
country_language_json = sys.argv[3]


data = pd.read_json(country_json)
data1 = pd.read_json(country_language_json)


ret_data = pd.merge(data[data["Continent"] == "North America"], data1[data1["IsOfficial"] == "T"], left_on='Code', right_on="CountryCode", how='left')[["Name","Language"]].groupby("Name")

for key, item in ret_data:
    if (isinstance(list(dict(ret_data.get_group(key)["Language"]).values())[0], str)):
        print(list(dict(ret_data.get_group(key)["Name"]).values())[0] + ", " + ", ".join(list(dict(ret_data.get_group(key)["Language"]).values())))
    else:
        print(list(dict(ret_data.get_group(key)["Name"]).values())[0] + ", None")

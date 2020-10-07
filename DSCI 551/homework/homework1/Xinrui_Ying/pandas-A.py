import pandas as pd
import sys

country_json = sys.argv[1]
city_json = sys.argv[2]
country_language_json = sys.argv[3]


data = pd.read_json(country_json)
data1 = pd.read_json(city_json)
print(pd.merge(data[data["Continent"] == "North America"], data1, left_on='Capital', right_on="ID", how='inner')[["Name_x", "Name_y"]])

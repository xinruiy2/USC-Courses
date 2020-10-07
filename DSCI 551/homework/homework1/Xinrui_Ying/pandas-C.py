import pandas as pd
import sys

country_json = sys.argv[1]
city_json = sys.argv[2]
country_language_json = sys.argv[3]


data = pd.read_json(country_json)

continents = data["Continent"].unique()

for continent in continents:
    # print(data[(data["GNP"]>5000) &(data["GNP"]<6000)]["Name"])
    if (data[(data["Continent"] == continent) & (data["GNP"]>10000)].shape[0] > 5):
        # print(data[(data["Continent"] == continent) & data["GNP"]>10000].shape[0])
        print(continent + " " + str(data[data["Continent"] == continent]["LifeExpectancy"].mean()))

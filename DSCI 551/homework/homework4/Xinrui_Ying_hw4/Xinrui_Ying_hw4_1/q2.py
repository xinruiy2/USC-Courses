import sys
import pyspark.sql.functions as fc
from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Q2")\
        .getOrCreate()

country = spark.read.json('country.json')
city = spark.read.json('city.json')
country[country.Continent == 'North America'].join(city, country.Capital == city.ID).select(country.Name.alias('country_name'), city.Name.alias('capital_name')).orderBy(country.Name).limit(10).show()

spark.stop()

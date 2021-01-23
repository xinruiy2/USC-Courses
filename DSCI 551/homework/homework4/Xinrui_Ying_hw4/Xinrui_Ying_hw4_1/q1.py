import sys
import pyspark.sql.functions as fc
from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Q1")\
        .getOrCreate()

country = spark.read.json('country.json')
country[(country.GNP > 100000) & (country.GNP < 500000) & (country.Continent == "Europe")].select('Name').show()

spark.stop()

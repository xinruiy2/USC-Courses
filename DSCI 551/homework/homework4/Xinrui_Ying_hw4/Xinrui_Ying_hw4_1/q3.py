import sys
import pyspark.sql.functions as fc
from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql.functions import concat_ws

spark = SparkSession\
        .builder\
        .appName("Q3")\
        .getOrCreate()

country = spark.read.json('country.json')
countrylanguage = spark.read.json('countrylanguage.json')

countrylanguage = countrylanguage[countrylanguage.IsOfficial == 'T'][["CountryCode", "Language"]]

country[country.Continent == 'North America'].join(countrylanguage, country.Code == countrylanguage.CountryCode).groupBy(country.Name).agg(fc.concat_ws(", ", fc.collect_list(countrylanguage.Language)).alias('Languages')).orderBy(country.Name).limit(10).show()

spark.stop()

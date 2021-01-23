import sys
import pyspark.sql.functions as fc
from pyspark.sql import SparkSession
from pyspark.sql import Window

spark = SparkSession\
        .builder\
        .appName("Q5")\
        .getOrCreate()

country = spark.read.json('country.json')
countrylanguage = spark.read.json('countrylanguage.json')


country.join(countrylanguage[(countrylanguage.IsOfficial == 'T') & (countrylanguage.Language == 'French')], country.Code == countrylanguage.CountryCode).groupBy(country.Continent).agg(fc.count("*").alias("cnt")).show()
spark.stop()

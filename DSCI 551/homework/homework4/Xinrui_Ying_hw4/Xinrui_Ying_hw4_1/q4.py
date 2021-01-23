import sys
import pyspark.sql.functions as fc
from pyspark.sql import SparkSession
from pyspark.sql import Window

spark = SparkSession\
        .builder\
        .appName("Q4")\
        .getOrCreate()

country = spark.read.json('country.json')
country[country.GNP > 10000].groupBy(country.Continent).agg(fc.mean('LifeExpectancy').alias('avg_le')).show()
spark.stop()

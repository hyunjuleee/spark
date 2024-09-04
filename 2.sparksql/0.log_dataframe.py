from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import split, col, max, min, mean

file_path = '/home/ubuntu/dmf/spark/2.sparksql/access.log'

spark = SparkSession.builder.getOrCreate()

schema = StructType([
    StructField('ip', StringType()),
    StructField('date', StringType()),
    StructField('time', StringType()),
    StructField('url', StringType()),
    StructField('status', IntegerType()),
    StructField('bytes', IntegerType()),
])

df = spark.read.csv(file_path, schema=schema, sep=' ')

# df.show()

df = df.withColumn('method', split(col('url'), ' ').getItem(0))
df = df.withColumn('path', split(col('url'), ' ').getItem(1))
df = df.withColumn('protocol', split(col('url'), ' ').getItem(2))

# df.show()

# status code가 200인 데이터만 출력
df_200 = df.filter(col('status') == 200)
# df_200.show()

# method GET & path product
df_product = df.filter((col('method') == 'GET') & (col('path').contains('product')))
# df_product.show()


# method, status code 별 count
df_group = df.groupBy('method', 'status').count()
# df_group.show()


# method, status code 별 bytes 최대, 최소, 평균
df_bytes = df.groupBy('method', 'status').agg(max('bytes'), min('bytes'), mean('bytes'))
df_bytes.show()
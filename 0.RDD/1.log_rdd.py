from pyspark import SparkContext

sc = SparkContext()

file_path = 'file:///home/ubuntu/dmf/spark/0.RDD/access.log'
lines = sc.textFile(file_path)

# print(lines.collect())

# 1.map
mapped_lines = lines.map(lambda line: line.split())
# print(lines.collect())
# lines.foreach(print)

# 2. filter
# 2-1.filter (4xx code만 출력)
def filter_4xx(line):
    return line[6][0] == '4'
filtered_lines = mapped_lines.filter(filter_4xx)
# filtered_lines.foreach(print)

# 2-2. filter (POST & /product)
def filter_post_product(line):
    return line[3] == '"POST' and 'product' in line[4]
filtered_log = mapped_lines.filter(filter_post_product)
filtered_log.foreach(print)

# 3. reduce
# 3-1. method 별 요청수
method_rdd = mapped_lines.map(lambda line: (line[3], 1)) \
    .reduceByKey(lambda a, b: a+b)
# method_rdd.foreach(print)

# 3-2. 시간대별 요청수
time_rdd = mapped_lines.map(lambda line: (line[2].split(':')[0], 1)) \
    .reduceByKey(lambda a, b: a+b)
# time_rdd.foreach(print)

# 4. groupby
# 4-1. status code, api method별 ip리스트 출력
def code_method(line):
    ip = line[0]
    status = line[6]
    method = line[3].replace('"', '')
    return (status, method), ip

group_by_rdd = mapped_lines.map(code_method) \
    .groupByKey().mapValues(list)
# group_by_rdd.foreach(print)

# 4.2 status code, api method별 ip 리스트 출력 => reduce 방식으로
reduce_rdd = mapped_lines.map(code_method) \
    .reduceByKey(lambda a, b: a + ' ' + b)
reduce_rdd.foreach(print)
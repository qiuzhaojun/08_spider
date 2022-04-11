"""
库名: studb
集合名: stuset
文档: {'name':'赵丽颖', 'age':34}
"""
import pymongo

# 1.创建数据库连接对象
conn = pymongo.MongoClient('localhost', 27017)
# 2.创建库对象
db = conn['studb']
# 3.创建集合对象
myset = db['stuset']
# 4.插入文档
myset.insert_one({'name':'小骨','age':34})























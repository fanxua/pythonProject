import pymongo
import csv

# 连接数据库
client = pymongo.MongoClient(host='localhost', port=27017)
# 获取数据库
db = client['text111']
# 获取集合
collection = db['zhanghao']

id=0
#指定文件路径
with open("order-20221209-100.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)

        email = row['email']
        password = row['password']
        apikey = row['apikey']
        id=id+1
        #print(email, password, apikey)
        result={
            "id": id,
            "email": email,
            "password": password,
            "apikey": apikey,



        }
        print(result)
        collection.insert_one(result)




"""
        db.collection.insert(
            {

            "email":email,
            "password":password,
            "apikey":apikey,
        })

        collection.insert_one(result)
        print(email,password,apikey)
    print("导入数据完成！")

"""




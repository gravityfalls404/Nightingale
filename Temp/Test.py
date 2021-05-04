import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Nightingale"]
mycol = mydb["Users"]

mydict = {"_id": 123456789, "username": "don", "stauts": "Online"}

mycol.insert_one(mydict)

for x in mycol.find({"_id": 123456}):
    print(x)
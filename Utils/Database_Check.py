import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["Nightingale"]
collection = database["Users"]



def show():
    if collection.count_documents({})==0:
        print("No Record")

    for x in collection.find():
        print(x)


def delete():
    collection.remove()

show()
# delete()
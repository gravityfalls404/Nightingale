import discord
from discord.ext.commands import Cog, command
from discord.ext import commands
import pymongo

class Database(Cog):
    def __init__(self, client):
        self.client = client
        self.user_collection = self._init_db_("Nightingale", "Users")




    @Cog.listener()
    async def on_member_join(self, member):
        _id = member.id
        name = member.name
        status = "Online"
        self.updateMemberinDB(_id, name, status)
        
    
    @Cog.listener()
    async def on_member_remove(self, member):
        _id = member.id
        status = "Offline"
        name = member.name
        self.updateMemberinDB(_id, name, status)

    @command()
    async def showdb(self, ctx):
        for user in self.user_collection.find():
            print(user)
        print("Done.")


    def _init_db_(self, database_name, collection):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = mongo_client[database_name]
        collection = database[collection]
        
        return collection
    

    def updateMemberinDB(self, _id, name, status):
        membercount = self.user_collection.count_documents({"_id": _id})
        if membercount == 0 :   #Memebr with _id does not exist
            user = {"_id": _id, "username": name, "status": status, "strikes": 0
            ,"Coins": 10}
            response = self.user_collection.insert_one(user)
            print("Member Created")
        else:
            query = {"_id": _id}
            new_val = {"$set": {"status": status}}
            self.user_collection.update_one(query,new_val)
            print("Member Updated")

    
        

def setup(client):
    client.add_cog(Database(client))
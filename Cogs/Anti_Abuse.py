from re import search
import discord
from discord.ext.commands import Cog, command
from discord.ext import tasks
from profanity_check import predict, predict_prob
import pymongo

"""
    This Class handles the anti abuse feature of the bot.
    Here I'm using prodanity check module by @{https://github.com/dimitrismistriotis/profanity-check}.
    The Predict function returns 1 for offensive messages.
    I'll be updating it with predic_prob in my next commit.
"""

class AnitAbuse(Cog):
    
    def __init__(self, client):
        self.client = client
        self.channel = None
        self.user_collection = self._init_db_("Nightingale", "Users")

    @Cog.listener()
    async def on_message(self, message):
        msg = message.content
        prediction = predict_prob([msg])
        self.channel = message.channel

        # Profanity check
        if prediction >=0.7 :    #Bad profanity
            await message.delete()

            query = {"_id": message.author.id}
            new_val = {"$inc": {"strike": 1}}
            self.user_collection.update_one(query, new_val)

            await self.channel.send(f"{message.author.mention} watch your language !!!")
    
        #Anti Advertisment
        if message.content.find("https://discord.gg/")!= -1:    #This message had a discord invite
            await message.delete()
            await message.author.send("Promoting is not allowed on the server!")

    def _init_db_(self, database_name, collection):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = mongo_client[database_name]
        collection = database[collection]
        
        return collection
            


def setup(client):
    client.add_cog(AnitAbuse(client))
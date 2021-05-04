import discord
from discord.ext.commands import Cog, command
from discord.ext import tasks
from profanity_check import predict, predict_prob


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

    @Cog.listener()
    async def on_message(self, message):
        msg = message.content
        prediction = predict([msg])
        self.channel = message.channel

        # Profanity check
        if prediction == 1 :
            await message.delete()
            await self.channel.send(f"{message.author.mention} watch your language !!!")
    
        #Anti Advertisment
        if message.content.find("https://discord.gg/")!= -1:    #This message had a discord invite
            await message.delete()
            await message.author.send("Promoting is not allowed on the server!")

            


def setup(client):
    client.add_cog(AnitAbuse(client))
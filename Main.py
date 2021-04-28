import discord
from Utils import Env
from discord.ext import commands, tasks
import os

Client = commands.Bot(command_prefix=Env.PREFIX, intents = discord.Intents.all())

def Init():
    for filename in os.listdir("./Cogs"):
        if(filename.endswith("py")):
            Client.load_extension(f'Cogs.{filename[:-3]}')

def Run():
    Init()
    Client.run(Env.BOT_TOKEN);


@Client.event
async def on_ready():
    print("Nightingale is Online!")


Run()
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv

load_dotenv()

Client = commands.Bot(command_prefix=os.getenv("PREFIX"), intents = discord.Intents.all())

def Init():
    for filename in os.listdir("./Cogs"):
        if(filename.endswith("py")):
            Client.load_extension(f'Cogs.{filename[:-3]}')

def Run():
    Init()
    Client.run(os.getenv("BOT_TOKEN"));


@Client.event
async def on_ready():
    print("Nightingale is Online!")


Run()
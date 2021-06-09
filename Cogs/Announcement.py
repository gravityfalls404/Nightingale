import discord
from discord.ext import commands, tasks
from discord.ext.commands import Cog, command
import random

class Announcement(Cog):
    def __init__(self, client):
        self.client = client
        self.flag = False
        self.embed_colors = [0x1f8b4c,0x3498db,0x1f8b4c,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x95a5a6,0x607d8b,0x607d8b,0x979c9f,0x979c9f,0x546e7a,0x546e7a,0x7289da,0x99aab5,0x36393F]
        self.emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😊", "😇", "🙂", "🙃", "😉", "😌", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🥸", "🤩", "🥳", "😏", "😳", "🤗", "🤭", "🤫", "🤠", "😈", "👹", "👺", "🤡", "👻", "👾", "🤖", "🎃", "😺", "😸", "😼", "👋", "🤚", "🖐", "✋", "🖖", "🤞", "🤟", "🤘", "🤙", "💃🏼", "🕺🏼" ] 
        # self.server_emoji = ["diamond_sword","Mega_Coin_Blue","Mega_Coin_White","steveface","golden_apple","Mega_Coin_Dark_Blue","diamond_pickaxe","diamond_shovel","Mega_Coin_Green","bow","lava_bucket"]
        self.title = "⭐New Announcement⭐"
        self.games = ["Megamine", "Minecraft", "Half Life", "Hermit", "With Life", "League of Legends", "Counter-Strike: Global Offensive", "Valorant", "Grand Theft Auto V"]
        


    @Cog.listener()
    async def on_message(self, message):
        if message.guild == None:
            return
        # announce_channel = discord.utils.get(message.guild.text_channels, name= "🔊｜𝖆𝖓𝖓𝖔𝖚𝖓𝖈𝖊𝖒𝖊𝖓𝖙𝖘")
        if self.flag and not message.author.bot :
           
            msg = message.content
            await message.delete()
            emoji_A =random.choice(self.emojis)
            emoji_B = random.choice(self.emojis)
            # logo_url = "attachment://Logo.jpg"
            # logo_file = discord.File("Cogs/Media/Logo.jpg",filename="Logo.jpg")

            embed = discord.Embed()
            embed.title = f'**{self.title}**'
            # embed.set_thumbnail(url = logo_url)
            embed.color = random.choice(self.embed_colors)
            embed.description = msg
            embed.set_footer(icon_url=message.author.avatar_url, text=f"by {message.author.name}")
            # await message.channel.send(embed = embed, file = logo_file)
            await message.channel.send(embed = embed)
            self.shoutlimit.cancel()

    @Cog.listener()
    async def on_ready(self):
        self.bot_status.start()

    @command()
    @commands.has_any_role("Admin")
    async def announce(self, ctx, title):
        await ctx.message.delete()
        if title != ".":
            self.title = f"**{random.choice(self.emojis)}"+title+f"{random.choice(self.emojis)}**"
        self.shoutlimit.start()
    
    @tasks.loop(minutes=1.0, count=6)
    async def shoutlimit(self):
        pass

    @shoutlimit.before_loop
    async def before_shout(self):
        self.flag=True
        

    @shoutlimit.after_loop
    async def after_shout(self):
        self.flag=False
        self.title = "⭐New Announcement⭐"

    @tasks.loop(minutes=10.0)
    async def bot_status(self):
        await self.client.change_presence(status = discord.Status.online, activity = discord.Game(random.choice(self.games)))


    
    

def setup(client):
    client.add_cog(Announcement(client))
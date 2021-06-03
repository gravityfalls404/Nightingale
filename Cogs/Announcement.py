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

    @Cog.listener()
    async def on_message(self, message):
        if message.guild == None:
            return
        announce_channel = discord.utils.get(message.guild.text_channels, name= "🔊｜announcements")
        if self.flag and not message.author.bot and message.channel == announce_channel:
           
            msg = message.content
            await message.delete()
            emoji_A =random.choice(self.emojis)
            emoji_B = random.choice(self.emojis)
            # logo_url = "attachment://Logo.jpg"
            # logo_file = discord.File("Cogs/Media/Logo.jpg",filename="Logo.jpg")

            embed = discord.Embed()
            embed.title = f'**{emoji_A} Firday Night {emoji_B}**'
            # embed.set_thumbnail(url = logo_url)
            embed.color = random.choice(self.embed_colors)
            embed.description = msg
            embed.set_footer(icon_url=message.author.avatar_url, text=f"by {message.author.name}")
            # await message.channel.send(embed = embed, file = logo_file)
            await message.channel.send(embed = embed)
            self.shoutlimit.cancel()

            

    @command()
    async def announce(self, ctx):
        await ctx.message.delete()
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




    
    

def setup(client):
    client.add_cog(Announcement(client))
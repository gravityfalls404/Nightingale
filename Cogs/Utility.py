import discord
from discord.ext import commands, tasks
from discord.ext.commands import Cog, command
import json, random
from tqdm import tqdm

class Utility(Cog):
    def __init__(self, client) :
        self.client = client
        self.embed_colors = [0x1f8b4c,0x3498db,0x1f8b4c,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x95a5a6,0x607d8b,0x607d8b,0x979c9f,0x979c9f,0x546e7a,0x546e7a,0x7289da,0x99aab5,0x36393F]
        self.emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😊", "😇", "🙂", "🙃", "😉", "😌", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🥸", "🤩", "🥳", "😏", "😳", "🤗", "🤭", "🤫", "🤠", "😈", "👹", "👺", "🤡", "👻", "👾", "🤖", "🎃", "😺", "😸", "😼", "👋", "🤚", "🖐", "✋", "🖖", "🤞", "🤟", "🤘", "🤙", "💃🏼", "🕺🏼" ] 
        self.guild_map = {}
        self.update_guild_map()

    @command()
    async def embed1(self, ctx):
        
        guild_name = ctx.message.guild.name
        guild_data = self.guild_map[guild_name]
        emoji_dict = guild_data[3]
    
        embed = discord.Embed()
        embed.title = "***Get Your Roles By Reacting***"
        desc = ""
        idx = 0
        for emoji, role_id in emoji_dict.items():
            role = discord.utils.get(ctx.message.guild.roles, id = role_id)
            desc += f"*{emoji} - {role.name}*"
            desc += "\n\n"

        embed.description = desc
        embed.color = random.choice(self.embed_colors)

        await ctx.message.delete()
        message = await ctx.send(embed = embed)
        
    

        for emoji, role_id in emoji_dict.items():
            await message.add_reaction(emoji)
    

    @command()
    async def embed2(self, ctx):
        
        guild_name = ctx.message.guild.name
        guild_data = self.guild_map[guild_name]
        emoji_dict = guild_data[4]
    
        embed = discord.Embed()
        embed.title = "***Get Your Roles By Reacting***"
        desc = ""
        idx = 0
        for emoji, role_id in emoji_dict.items():
            role = discord.utils.get(ctx.message.guild.roles, id = role_id)
            desc += f"*{emoji} - {role.name}*"
            if idx%2==0:
                desc+="\t\t"
            else:
                desc+="\n\n"

            idx+=1

        embed.description = desc
        embed.color = random.choice(self.embed_colors)

        await ctx.message.delete()
        message = await ctx.send(embed = embed)
        
    

        for emoji, role_id in emoji_dict.items():
            await message.add_reaction(emoji)



    def update_guild_map(self):
        roles_fp = open("Utils/Roles.json")
        self.guild_map = json.load(roles_fp)

    @command()
    async def getroles(self,ctx):
        members_list = ctx.message.guild.members
        member = ctx.message.author
        for member in tqdm(members_list):
            if member.bot:
                continue
            print(member.name)
            try:
                embed = discord.Embed()
                embed.title = f"***Welcome to Gulag {member.name}***"
                embed.description = f"I'm Nightingale the All_IN_1 Bot by <@732975737140674592>.\n\n To get the full experice please get your roles at <#849654103323050085> \n\n "
                embed.set_thumbnail(url= member.avatar_url)

                await member.send(embed= embed)
                await ctx.message.delete()
            except:
                continue



def setup(client):
    client.add_cog(Utility(client))
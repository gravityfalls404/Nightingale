import discord
from discord.ext.commands import Cog, command
import random
from tqdm import tqdm
class Welcome(Cog):
    def __init__(self, client):
        self.client = client
        self.info = []
        self.greetings = []
        self.utils()
        self.logo_url = None
        self.logo_file = None
        self.embed_colors = [0x3498db,0x1f8b4c,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x95a5a6,0x607d8b,0x607d8b,0x979c9f,0x979c9f,0x546e7a,0x546e7a,0x7289da,0x99aab5,0x36393F]
        self.emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😊", "😇", "🙂", "🙃", "😉", "😌", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🥸", "🤩", "🥳", "😏", "😳", "🤗", "🤭", "🤫", "🤠", "😈", "👹", "👺", "🤡", "👻", "👾", "🤖", "🎃", "😺", "😸", "😼", "👋", "🤚", "🖐", "✋", "🖖", "🤞", "🤟", "🤘", "🤙", "💃🏼", "🕺🏼" ] 

    @Cog.listener()
    async def on_ready(self):
        # print("Welcome Ready.")
        pass
    def utils(self):
        with open("Cogs/Media/greetings.txt") as file:
            greetings = file.readlines()
            greetings = [greetings.strip() for greetings in greetings]
            self.greetings = [x for x in greetings]

    @Cog.listener()
    async def on_member_join(self, member):
        about_us = discord.utils.get(member.guild.text_channels, name = "📝｜about")
        general = discord.utils.get(member.guild.text_channels, name="💬｜general")
        # await self.general.send(f'{member.mention} is here')
        rules = discord.utils.get(member.guild.text_channels, name = "✔｜rules")
        # self.logo_url = "attachment://Logo.jpg"
        # self.logo_file = discord.File("Cogs/Media/Logo.jpg",filename="Logo.jpg")
        """
        Embed for the new members Dm.
        
        """

        welcome = discord.utils.get(member.guild.text_channels, name = "😃｜welcome")
        # embed = discord.Embed()
        # embed.description = f"""Dear, {member.mention}\n
        #     We {welcome.mention} you to Mega Mine! This server is intended to surpass even the best of Minecraft Multiplayer servers, offering more games and options to it's members. Our most popular option is SMP (Survival Multi Player). We pride our freedom in our servers to the highest degree.\n
        #     While you're here, we ask that you review the channels in the important category. Review the rules, about us, etc. This'll help navigation of the server run much more smoothly. If you have any questions, ask a helper+\n
        #     Thank you for joining us! We are the beginning of a great future!\n

        # Signed,
        # Mega Mine Staff"""
        # embed.color = random.choice(self.embed_colors)
        # embed.set_thumbnail(url=self.logo_url)
        # embed.set_footer(text = " Keep Mining ", icon_url=self.logo_url)
        # await member.send(embed = embed, file= self.logo_file)

        """
        Embed for the welcome channel
        """
        line1 = random.choice(self.greetings).format(member.mention) + " " + random.choice(self.emojis)
        line2 = f'You\'re our {len(member.guild.members)}th member '
        line3 = f" Before Going In server Kindly read rules & regulations of the server in {rules.mention}"
        line4 = f"Here is your Robo mate"
        # line5 = f"Learn More about the Server at {about_us.mention}"
        avatar = member.avatar_url
        
        embed = discord.Embed()
        embed.set_image(url=f"https://robohash.org/{member.name}")
        embed.description = f"*➡️{line1}\n\n {line2}\n\n➡️ {line3}\n\n➡️ {line4}\n\n*"
        embed.color = random.choice(self.embed_colors)
        embed.set_thumbnail(url=avatar)
        await welcome.send(embed= embed)
    
    @command()
    async def welcome(self, ctx):
        
        members_list = ctx.message.guild.members
        print(len(members_list))

        for member in tqdm(members_list):
            if member.bot:
                continue
            about_us = discord.utils.get(member.guild.text_channels, name = "📝｜about")
            general = discord.utils.get(member.guild.text_channels, name="💬｜general")
            # await self.general.send(f'{member.mention} is here')
            rules = discord.utils.get(member.guild.text_channels, name = "✔｜rules")
            # self.logo_url = "attachment://Logo.jpg"
            # self.logo_file = discord.File("Cogs/Media/Logo.jpg",filename="Logo.jpg")
            """
            Embed for the new members Dm.
            
            """

            welcome = discord.utils.get(member.guild.text_channels, name = "😃｜welcome")
            # embed = discord.Embed()
            # embed.description = f"""Dear, {member.mention}\n
            #     We {welcome.mention} you to Mega Mine! This server is intended to surpass even the best of Minecraft Multiplayer servers, offering more games and options to it's members. Our most popular option is SMP (Survival Multi Player). We pride our freedom in our servers to the highest degree.\n
            #     While you're here, we ask that you review the channels in the important category. Review the rules, about us, etc. This'll help navigation of the server run much more smoothly. If you have any questions, ask a helper+\n
            #     Thank you for joining us! We are the beginning of a great future!\n

            # Signed,
            # Mega Mine Staff"""
            # embed.color = random.choice(self.embed_colors)
            # embed.set_thumbnail(url=self.logo_url)
            # embed.set_footer(text = " Keep Mining ", icon_url=self.logo_url)
            # await member.send(embed = embed, file= self.logo_file)

            """
            Embed for the welcome channel
            """
            line1 = random.choice(self.greetings).format(member.mention) + " " + random.choice(self.emojis)
            line2 = f'You\'re our {len(member.guild.members)}th member '
            line3 = f" Before Going In server Kindly read rules & regulations of the server in {rules.mention}"
            line4 = f"Here is your Robo mate"
            # line5 = f"Learn More about the Server at {about_us.mention}"
            avatar = member.avatar_url
            
            embed = discord.Embed()
            embed.set_image(url=f"https://robohash.org/{member.name}")
            embed.description = f"*➡️{line1}\n\n {line2}\n\n➡️ {line3}\n\n➡️ {line4}\n\n*"
            embed.color = random.choice(self.embed_colors)
            embed.set_thumbnail(url=avatar)
            await welcome.send(embed= embed)
        await ctx.message.delete()


        
    

def setup(client):
    client.add_cog(Welcome(client))
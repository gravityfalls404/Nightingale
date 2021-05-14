from os import name
import random
from discord.embeds import EmptyEmbed
import pymongo
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Cog, command
import requests, json, time

class Points_Game(Cog):
    def __init__(self, client):
        self.client = client
        self.questions = []
        self.numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        self.bin = ["👍","👎"]
        self.polls = []
        self.embed_colors = [0x3498db,0x1f8b4c,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x95a5a6,0x607d8b,0x607d8b,0x979c9f,0x979c9f,0x546e7a,0x546e7a,0x7289da,0x99aab5,0x36393F]
        self.start_time = dict()
        self.expire_time = 3600     #1 hr
        self.participants = dict()

    @command()
    async def quiz(self, ctx):

        await ctx.message.delete()

        if len(self.questions) == 0:
            self.populate_questions()
        
        
        ques = self.questions.pop(random.randrange(len(self.questions)))

        #Question's attribute

        prompt = ques["question"]
        catrgory = ques["category"]
        difficulty = ques["difficulty"]
        options = ques["incorrect_answers"]
        options.append(ques["correct_answer"])
        ans = ques["correct_answer"]
        indx = options.index(ans)
        numop = len(options)
        random.shuffle(options)

        embed = discord.Embed()
        embed.color = random.choice(self.embed_colors)
        embed.title = "Pop Quiz"
        embed.description = f"***{prompt}***"

        if numop == 4 :
            for idx in range(len(options)):
                embed.add_field(name=f"{self.numbers[idx]}.{options[idx]}", value="*", inline=False)
        
        else:
            embed.add_field(name= f"{self.bin[0]}.True", value="*", inline=False)
            embed.add_field(name = f"{self.bin[1]}.Frue", value="*", inline=False) 
        
        response = await ctx.send(embed = embed)
        self.start_time[response.id] = time.time()
        self.participants[response.id] = []
        
        if numop == 4: 
            for emoji in self.numbers:
                    await response.add_reaction(emoji)
        else:
            for emoji in self.bin:
                    await response.add_reaction(emoji)

        self.polls.append((response.channel.id, response.id))




    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        if payload.message_id in self.start_time:
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            flag = True
            if (payload.member in self.participants[payload.message_id]):
                flag = False
                await message.remove_reaction(payload.emoji, payload.member)

            elif(abs(self.start_time[payload.message_id]-time.time())>self.expire_time):
                await message.remove_reaction(payload.emoji, payload.member)
                
            elif(payload.emoji.name in [reaction.emoji for reaction in message.reactions]):
                await message.remove_reaction(payload.emoji, payload.member)

            if flag:
                self.participants[payload.message_id].append(payload.member)
                

    def populate_questions(self):
        headers = {
        'Cookie': 'PHPSESSID=3d376b99b1dcc8d1bd5bb3380e52e399'
        }
        response = requests.request("GET", "https://opentdb.com/api.php?amount=50", headers=headers, data={})
        
        if response.status_code !=200:
            return False

        response = json.loads(response.text)
        self.questions = response["results"]

        return True




def setup(client):
    client.add_cog(Points_Game(client))

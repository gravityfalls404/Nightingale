from os import name
import random
from discord.embeds import EmptyEmbed
import pymongo
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Cog, command
import requests, json, time

from requests.models import parse_url

class Points_Game(Cog):
    def __init__(self, client):
        self.client = client
        self.questions = []
        self.numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        self.bin = ["👍🏻","👎🏻"]
        self.polls = []
        self.embed_colors = [0x3498db,0x1f8b4c,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x95a5a6,0x607d8b,0x607d8b,0x979c9f,0x979c9f,0x546e7a,0x546e7a,0x7289da,0x99aab5,0x36393F]
        self.ques_dict = dict()
        self.expire_time = 60     #1 hr
        self.participants = dict()
        self.user_collection = self._init_db_("Nightingale", "Users")


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
        self.ques_dict[response.id] = {"time":time.time(), "ans": indx, "long": (numop==4)}
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

        if payload.message_id in self.ques_dict:
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)

            flag = True
            if (payload.member.id in self.participants[payload.message_id]):      #if the member has already reacted, remove new reaction
                flag = False
                await message.remove_reaction(payload.emoji, payload.member)
                print("line 86")

            elif(abs(self.ques_dict[payload.message_id]["time"]-time.time())>self.expire_time):    #The poll has expired
                await message.remove_reaction(payload.emoji, payload.member)
                print("line 90")
                
            elif(payload.emoji in [reaction.emoji for reaction in message.reactions]):     #If a new type of reaction is added remove it
                await message.remove_reaction(payload.emoji, payload.member)
                print("line 94")    

            if flag:
                self.participants[payload.message_id].append({"participant_Id":payload.member.id, "reaction": payload.emoji.name})    #If the paricipant is new add him to the participants list
                print("line 98")


    # @tasks.loop(hours=1.0)
    @command()
    async def results(self, ctx):

        curr_time = time.time()
        ques_dict_temp = self.ques_dict.copy()

        for id, data in ques_dict_temp.items():

            if abs(self.ques_dict[id]["time"] - curr_time) > self.expire_time:
                winners = []
                ans = -1
                if data["long"]:
                    ans =self.numbers[data["ans"]]
                else:
                    ans = self.bin[data["ans"]]

                for part in self.participants[id]:
                    if ans == part["reaction"]:
                        winners.append(part["participant_Id"])

                self.add_points(winners, 100)
                self.ques_dict.pop(id)
                self.participants.pop(id)



    def populate_questions(self):
        headers = {
        'Cookie': 'PHPSESSID=3d376b99b1dcc8d1bd5bb3380e52e399'
        }
        response = requests.request("GET", "https://opentdb.com/api.php?amount=5", headers=headers, data={})    #Change this to 50
        
        if response.status_code !=200:
            return False

        response = json.loads(response.text)
        self.questions = response["results"]

        return True

    def add_points(self, _ids, points):
        try:
            query = {"_id": {"$in" : _ids}}
            new_val = {"$inc": {"Coins":points}}
            self.user_collection.update(query, new_val, multi=True)    
            print("Updated")
            return True
        except:
            
            print("DB Error")
            return None

    def _init_db_(self, database_name, collection):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = mongo_client[database_name]
        collection = database[collection]
        
        return collection




def setup(client):
    client.add_cog(Points_Game(client))

import discord
from discord.ext.commands import command, Cog
from discord.ext import tasks
import time
from googlesearch import search
import requests
from Utils import Env
import json
from Media import Store
import random


class AD_HOC(Cog):
    def __init__(self, client):
        self.client = client
        self.embed_colors = [0x3498db,0x1f8b4c,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0xa84300,0xe74c3c,0x992d22,0x95a5a6,0x95a5a6,0x607d8b,0x607d8b,0x979c9f,0x979c9f,0x546e7a,0x546e7a,0x7289da,0x99aab5,0x36393F]


    @command()
    async def ping(self, ctx):
        await ctx.trigger_typing()
        time.sleep(1)
        await ctx.send(f"**Pong {round(self.client.latency*1000)}ms!🧘🏻‍♂️**")

    @command()
    async def lookup(self, ctx):
        results = search(ctx.message.content, num_results=1)
        await ctx.send("*Searching...*"+"🔍")
        await ctx.trigger_typing()
        time.sleep(2)
        await ctx.channel.purge(limit=1)
        await ctx.send(results[0])
    
    @command()
    # @command.has_any_role("<Role Name>")
    async def clean(self, ctx, limit):
        await ctx.channel.purge(limit=int(limit)+1)

    @command()
    async def covid(self, ctx, country):

        url = "https://covid-19-data.p.rapidapi.com/country"
        querystring = {"name":country}
        headers = {
            'x-rapidapi-key': Env.COVIDAPI_KEY,
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)

        if len(response)==0:
            await ctx.send("*Enter a valid country name !*")
            return
        response = response[0]
        country = response["country"]
        code = response["code"]
        confirmed = response["confirmed"]
        recovered = response["recovered"]
        deaths = response["deaths"]


        embed = discord.Embed()
        embed.color = random.choice(self.embed_colors)
        embed.title = f"*Covid Report of {country.upper()}*"
        logo_url = "attachment://Logo.jpg"
        logo_file = discord.File("Logo.jpg",filename="Logo.jpg")
        embed.set_author(icon_url=logo_url, name="Nightingale")
        embed.set_thumbnail(url=f"https://flagcdn.com/256x192/{code.lower()}.png")
        embed.add_field(name = "*Country*", value = country.upper(), inline=False)
        embed.add_field(name = "*Confirmed Cases*", value = confirmed, inline=False)
        embed.add_field(name = "*Recovered*", value = recovered, inline=False)
        embed.add_field(name = "*Total Deaths*", value = deaths, inline=False)
        await ctx.send(file = logo_file,embed=embed)



def setup(client):
    client.add_cog(AD_HOC(client))
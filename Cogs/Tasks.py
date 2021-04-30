import discord
from discord.ext.commands import Cog, command
from discord.ext import tasks
import time

"""
Class that'll contain all the runnable tasks.
These tasks are run periodically to make changes to the bot or server.
Read more about it at @{https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html?highlight=tasks}
"""


class Tasks(Cog):
    def __init__(self, client):
        self.client = client
        self.total_guildMembers = 0
    
    """
    # This Task will set the status to the total memers in all the servers it is being used in every 5 Minutes.
    """

    @Cog.listener()
    async def on_ready(self):
        count = 0
        guilds = self.client.guilds
        for guild in guilds:
            count += guild.member_count
    
        self.setStatus.start()
    @tasks.loop(minutes = 5.0)
    async def setStatus(self):
        await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"{self.total_guildMembers} Members"))


def setup(client):
    client.add_cog(Tasks(client))
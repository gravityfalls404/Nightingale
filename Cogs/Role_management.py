import discord
from discord.ext import commands, tasks
from discord.ext.commands import Cog, command
import json

"""""""""""""""""""""""""""""""""""""""
#   <GuildMap>
#       It will store guild names as keys vs a list of details.
#       This list will look like this [ `Guild_ID`, `Roles_Channel_ID` , `Message_ID vs Emoji_list Dict `, `Emoji vs Roles_ID Dict`]
#
#
"""""""""""""""""""""""""""""""""""""""

class Roles(Cog):
    def __init__(self, client):
        self.client =  client
        self.guild_map = {}
        self.update_guild_map()
    
    @Cog.listener()
    async def on_message(self, message):
        pass
       


    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        ##Condition check for the reaction

        #No emoji restrictions for bot
        if payload.member.bot:
            return

        #Checking the condition that the reaction is useful for roles
        guild_id = payload.guild_id
        guild_data = []

        for guild_name in self.guild_map:
            guild_id = self.guild_map[guild_name][0]
            role_channel_id = self.guild_map[guild_name][1]

            if payload.guild_id == guild_id and payload.channel_id == role_channel_id:
                guild_data = self.guild_map[guild_name]
                break

        else:
            return


        #Condition check that the raction is not vague
        message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)

        # if(str(payload.emoji) not in [str(reaction.emoji) for reaction in message.reactions]):     
        #     await message.remove_reaction(payload.emoji, payload.member)
        #     return
        ###############
        reacted_emoji = str(payload.emoji)
        emoji_dict = guild_data[3]
        
        role = discord.utils.get(payload.member.guild.roles, id = emoji_dict[reacted_emoji])
        await payload.member.add_roles(role)
        
    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        ##Condition check for the reaction

        #Checking the condition that the reaction is useful for roles in roles_channel
        guild_id = payload.guild_id
        guild_data = []

        for guild_name in self.guild_map:
            guild_id = self.guild_map[guild_name][0]
            role_channel_id = self.guild_map[guild_name][1]

            if payload.guild_id == guild_id and payload.channel_id == role_channel_id:
                guild_data = self.guild_map[guild_name]
                break

        else:
            return


        reacted_emoji = str(payload.emoji)
        emoji_dict1 = guild_data[3] 

        guild = self.client.get_guild(guild_data[0])
        member = guild.get_member(payload.user_id)

        if reacted_emoji not in emoji_dict1.keys():
            return

        role = discord.utils.get(guild.roles, id = emoji_dict1[reacted_emoji])
        await member.remove_roles(role)

            

        

        

    def update_guild_map(self):
        roles_fp = open("Utils/Roles.json")
        self.guild_map = json.load(roles_fp)





def setup(client):
    client.add_cog(Roles(client))
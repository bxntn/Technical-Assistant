from enum import Enum
from typing import Optional
import disnake, asyncio
from disnake.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import os



class Check(commands.Cog):

    def __init__(self, bot:commands.Bot):
        self.bot = bot

        

    @commands.slash_command()
    async def check_homework(self,inter:disnake.ApplicationCommandInteraction,guild_id,channel_id,start_time,end_time):
        load_dotenv()
        ADMIN = os.getenv('ADMIN')
        print(ADMIN)
        await inter.send("found this command")
        guilds = self.bot.guilds
        guild = self.bot.get_guild(int(guild_id))
        # if inter.author.id not in self.admins:
        #     inter.send("You are not allowed to use this command")
        #     return
        if guild:
            channel = guild.get_channel(int(channel_id))
            if channel:
                start = start_time.split("/")
                end = end_time.split("/")
                start_date = datetime(int(start[0]),int(start[1]),int(start[2]))
                end_date = datetime(int(end[0]),int(end[1]),int(end[2]))
                
                messages = await channel.history(limit=123,before = end_date,after =start_date).flatten()
                for message in messages:
                    # for reaction in message.reactions:
                    #     if reaction.emoji.id == "":
                    #         print()
                    if len(message.reactions) != 0:
                        print(f"The message : ([{message.id}] {message.content}) from authorID : {message.author.id}, author name : {message.author.name}#{message.author.discriminator} ")
                    
            else:
                await inter.send(f"The channel with ID{channel_id} is not found")
        else:
            await inter.send(f"Guild with ID {guild_id} is not found")


        # channel = self.bot.get_guild(guild_id).get_channel(channel_id)
        # messages = await channel.history(limit = 200).flatten()
        # for message in messages:
        #     await inter.send(f"message : {message.content} has following sticker\n")
        #     for sticker in message.stickers:
        #         await inter.send(sticker.id)


def setup(bot) -> None:
	""" Bind this cog to the bot """
	bot.add_cog(Check(bot))

    

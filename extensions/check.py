from enum import Enum
from typing import Optional
import disnake
import asyncio
from disnake.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import os,csv
import numpy as np
import pandas as pd


class Check(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    async def check_homework(self, inter: disnake.ApplicationCommandInteraction, name, point, guild_id, channel_id, start_time, end_time):
        await inter.send("found this command")
        guild = self.bot.get_guild(int(guild_id))
        # if inter.author.id not in self.admins:
        #     inter.send("You are not allowed to use this command")
        #     return
        db = np.empty([0,4])
        if guild:
            channel = guild.get_channel(int(channel_id))
            if channel:
                start = start_time.split("/")
                end = end_time.split("/")
                start_date = datetime(
                    int(start[0]), int(start[1]), int(start[2]))
                end_date = datetime(int(end[0]), int(end[1]), int(end[2]))

                messages = await channel.history(limit=123, before=end_date, after=start_date).flatten()
                for message in messages:
                    # for reaction in message.reactions:
                    #     if reaction.emoji.id == "":
                    #         print()
                    Mid = message.id
                    Did = message.author.id
                    Aid = message.author.name +'#'+ message.author.discriminator
                    if len(message.reactions) != 0:
                        # print(
                        #     f"The message : ([{message.id}] {message.content}) from authorID : {message.author.id}, author name : {message.author.name}#{message.author.discriminator} ")
                        index = np.argwhere(db == f"'{Did}'")
                        if len(index) != 0:
                            db[index[0][0]][3] = point
                            db[index[0][0]][2] = f"'{Mid}'"
                        else:
                            data = np.array([[f"'{Did}'", Aid, f"'{Mid}'", int(point)]])
                            db = np.append(db,data,axis=0)
                    else:
                        index = np.argwhere(db == f"'{Did}'")
                        if len(index) == 0:
                            data = np.array([[f"'{Did}'", Aid, f"'{Mid}'", 0]])
                            db = np.append(db,data,axis=0)
        
                    
                df = pd.DataFrame(db, columns=['DiscordID','AuthorID','MessageID','Point'])
                df = df.astype({'DiscordID':'string','MessageID':'string'})
                print(df)
                df.index = list(df['DiscordID'])
                #self.check_dir(f'{name}.csv')
                df.to_csv(f'database/{name}.csv',index = False)

            else:
                await inter.send(f"The channel with ID{channel_id} is not found")
        else:
            await inter.send(f"Guild with ID {guild_id} is not found")

    def check_dir(self,file_name):
        directory = os.path.dirname(file_name)
        print('check the directory')
        if not os.path.exists(directory):
            os.makedirs(directory) 


def setup(bot) -> None:
    """ Bind this cog to the bot """
    bot.add_cog(Check(bot))

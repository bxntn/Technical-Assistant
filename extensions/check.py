from __future__ import print_function

import disnake
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from disnake.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import os
import csv
import numpy as np
import pandas as pd
from enum import Enum


class Check(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    @commands.default_member_permissions(manage_guild=False, moderate_members=True)
    async def check_homework(self, inter: disnake.ApplicationCommandInteraction, homework_name, point, guild_id, channel_id, start_time, end_time):

        guild = self.bot.get_guild(int(guild_id))
        # if inter.author.id not in self.admins:
        #     inter.send("You are not allowed to use this command")
        #     return

        # Gathering data
        db = np.empty([0, 4])
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
                    Aid = message.author.name + '#' + message.author.discriminator
                    if len(message.reactions) != 0:
                        # print(
                        #     f"The message : ([{message.id}] {message.content}) from authorID : {message.author.id}, author name : {message.author.name}#{message.author.discriminator} ")
                        index = np.argwhere(db == str(Did))
                        if len(index) != 0:
                            db[index[0][0]][3] = int(point)
                            db[index[0][0]][2] = Mid
                        else:
                            data = np.array(
                                [[str(Did), Aid, Mid, int(point)]])
                            db = np.append(db, data, axis=0)
                    else:
                        index = np.argwhere(db == str(Did))
                        if len(index) == 0:
                            data = np.array([[str(Did), Aid, Mid, int(0)]])
                            db = np.append(db, data, axis=0)
            else:
                await inter.send(f"The channel with ID{channel_id} is not found")
            for member in guild.members:
                Did = member.id
                Aid = member.name + '#' + member.discriminator
                index = np.argwhere(db == str(Did))
                if len(index) == 0:
                    data = np.array([[str(Did),Aid,None,0]])
                    db = np.append(db,data,axis=0)
        else:
            await inter.send(f"Guild with ID {guild_id} is not found")
        print('collect db succesful\n')
        await inter.send("Collecting data successful")
        # push data to Google Sheet
        creds = self.bot.creds
        print("cred checked\n")


        try:

            service = build('sheets', 'v4', credentials=creds)
            print("service build successful\n")
            values = db.tolist()
            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range=f"{homework_name}!A2:D",
                valueInputOption= 'USER_ENTERED', body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

        

def setup(bot) -> None:
    """ Bind this cog to the bot """
    bot.add_cog(Check(bot))

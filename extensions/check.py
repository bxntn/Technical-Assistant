from __future__ import print_function

import disnake
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from disnake.ext import commands
from datetime import datetime
import numpy as np
import pandas as pd
from enum import Enum


class Check(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    @commands.default_member_permissions(manage_guild=True, moderate_members=True)
    async def check_homework(self, inter: disnake.ApplicationCommandInteraction, homework, point, guild_id, channel_id, start_time, end_time):

        creds = self.bot.creds

        try:
            service = build('sheets', 'v4', credentials=creds)
            print("service build successful\n")
            result = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='info!A1:AB').execute()
            rows = result.get('values', [])

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

        df = pd.DataFrame(rows[1:],columns=rows[0])
        board = df[['ID','discord_dev_id','Discord ID','Email ที่ใช้ลงทะเบียน website','ชื่อ','นามสกุล']].values
        

        guild = self.bot.get_guild(int(guild_id))

        # Gathering data
        if guild:
            for row in board:
                row[-2] = None
                row[-1] = 0

            channel = guild.get_channel(int(channel_id))
            if channel:
                start = start_time.split("/")
                end = end_time.split("/")
                start_date = datetime(
                    int(start[0]), int(start[1]), int(start[2]))
                end_date = datetime(int(end[0]), int(end[1]), int(end[2]))

                messages = await channel.history(limit=400, before=end_date, after=start_date).flatten()
                for message in messages:
                    Mid = message.id
                    Did = message.author.id
                    Aid = message.author.name + '#' + message.author.discriminator
                    reactions = message.reactions
                    emojis = [reaction.emoji for reaction in reactions]
                    index = np.argwhere(board == str(Did))

                    #if found in database
                    if len(index) != 0:
                        board[index[0][0]][-2] = str(Mid)
                        if '✅' in emojis:  
                            board[index[0][0]][-1] = int(point)
            else:
                await inter.send(f"The channel with ID{channel_id} is not found")
        else:
            await inter.send(f"Guild with ID {guild_id} is not found")
        print('collect db succesful\n')
        await inter.send("Collecting data successful")
        
        
        # push data to Google Sheet
        creds = self.bot.creds
        print("cred checked\n")

        try:
            values = board.tolist()
            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range=f"{homework}!A2:F",
                valueInputOption= 'USER_ENTERED', body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    @check_homework.autocomplete("homework")
    async def key_autocomp(inter: disnake.ApplicationCommandInteraction, user_input: str):
        KEY_OF = ("spot_homework","introduce")
        return [ key
            for key in KEY_OF
            if user_input.lower() in key.lower()
        ]

    @check_homework.autocomplete('guild_id')
    async def guild_autocomp(self,inter:disnake.ApplicationCommandInteraction, guild_name: str):
        self.bot.guilds

def setup(bot) -> None:
    """ Bind this cog to the bot """
    bot.add_cog(Check(bot))

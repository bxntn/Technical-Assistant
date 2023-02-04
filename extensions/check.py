from __future__ import print_function

import disnake
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from disnake.ext import commands
from datetime import datetime
import numpy as np
import pandas as pd


class Check(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    @commands.default_member_permissions(manage_guild=True, moderate_members=True)
    async def check_homework(self, inter: disnake.ApplicationCommandInteraction, homework, point,channel_name, start_time, end_time):

        creds = self.bot.creds

        try:
            service = build('sheets', 'v4', credentials=creds)
            print("service build successful\n")
            result = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='info!A:Y').execute()
            rows = result.get('values', [])

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

        df = pd.DataFrame(rows[1:], columns=rows[0])
        board = df[['ID', 'discord_dev_id', 'Discord ID',
                    'Email ที่ใช้ลงทะเบียน website', 'ชื่อ', 'นามสกุล']].values
        
        for row in board: #Initiative data
            row[-2] = None
            row[-1] = 0

        guilds = self.bot.guilds
        channels = []
        for guild in guilds:
            for cn in guild.text_channels:
                channels.append(cn)
        channelMap = {}
        for c in channels:
            channelMap[f"[{c.guild.name}] {c.name}"] = int(c.id)


        # Gathering data
        channel_id = channelMap[channel_name]
        

        channel = self.bot.get_channel(int(channel_id))
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

                # if found in database
                if len(index) != 0:
                    board[index[0][0]][-2] = str(Mid)
                    if '✅' in emojis:
                        board[index[0][0]][-1] = int(point)
            print('collect db succesful\n')
        else:
            await inter.send(f"The channel with ID{channel_id} is not found")

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
                spreadsheetId=self.bot.config['googlesheet'][
                    'main_sheet'], range=f"{homework}!A2:F",
                valueInputOption='USER_ENTERED', body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


    @check_homework.autocomplete('channel_name')
    async def channel_autocomp(self,inter:disnake.ApplicationCommandInteraction, channel_name: str):
        guilds = self.bot.guilds
        channels = []
        for guild in guilds:
            for cn in guild.text_channels:
                channels.append(cn)
        
        CHANNEL_OF = [f"[{ch.guild.name}] {ch.name}" for ch in channels]
        return [ key
            for key in CHANNEL_OF
            if channel_name.lower() in key.lower()
        ]


def setup(bot) -> None:
    """ Bind this cog to the bot """
    bot.add_cog(Check(bot))

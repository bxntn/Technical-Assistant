import disnake
from disnake.ext import commands

import pandas as pd
import numpy

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Announcement(commands.Cog):
    """ give a password for bootcamp or Java-app """
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.cooldown(1,1)
    @commands.default_member_permissions(manage_guild=True, moderate_members=True)
    @commands.slash_command(name = 'announce',
                            description= 'Announce a score descending',
                            dm_permission=False)
    async def annouce(
        self,
        inter:disnake.ApplicationCommandInteraction,channel_id
        # key_of:str
        
    ):
        """
        Sending back password to author

        Args:
            inter (disnake.GuildCommandInteraction): _description_
        """

        SCORE_COL = ''
        
        creds = self.bot.creds
        # pylint: disable=maybe-no-member
        
        try:
            service = build('sheets', 'v4', credentials=creds)

            result = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='total_score!A:B').execute()
            rows = result.get('values', [])

            data = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='total_score!A:B').execute()
            datarows = data.get('values', [])

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
        df = pd.DataFrame(rows[1:],columns=rows[0])
        
        temp_board = df.sort_values(by=['total_score'],axis=0,ascending=False)
        board = temp_board[['ID','total_score']].values.tolist()
        
        guild_id = inter.guild_id
        guild = self.bot.get_guild(guild_id)
        
        name = []
        message = f'**คะแนนรวมสูงสุด 10 อันดับแรก**'
        for i in range(10):
            message += f"\n{board[i][0]} with score {board[i][1]}"
        channel = self.bot.get_channel(int(channel_id))
        await channel.send(content=message)

    
    
def setup(bot) -> None:
	""" Bind this cog to the bot """
	bot.add_cog(Announcement(bot))
 
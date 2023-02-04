import disnake
from disnake.ext import commands

import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
import pandas as pd


class Request(commands.Cog):
    """ give a password for bootcamp or Java-app """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.cooldown(1, 1)
    @commands.dm_only()
    # @commands.default_member_permissions(manage_guild=True, moderate_members=True)
    @commands.command(name='profile',
                            description='Get password for bootcamp website')
    async def request_key(
        self,
        inter: disnake.ApplicationCommandInteraction,
        # key_of:str

    ):
        """
        Sending back password to author

        Args:
            inter (disnake.GuildCommandInteraction): _description_
        """

        BC_COL = ''
        JAVA_COL = ''

        creds = self.bot.creds
        # pylint: disable=maybe-no-member

        try:
            service = build('sheets', 'v4', credentials=creds)

            dataResult = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='info!A1:Y').execute()
            scoreResult = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='total_score!A1:B').execute()
            accountResult = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='preflop_account!A1:C').execute()
            datarows = dataResult.get('values', [])
            scorerows = scoreResult.get('values', [])
            accountrows = accountResult.get('values',[])

            datadf = pd.DataFrame(datarows[1:], columns=datarows[0])
            databoard = datadf[['discord_dev_id','ID']].values
            accountdf = pd.DataFrame(accountrows[1:], columns=accountrows[0])
            accountboard = accountdf[['ID','Email','Password']].values
            scoredf = pd.DataFrame(scorerows[1:], columns=scorerows[0])
            scoreboard = scoredf[['ID','total_score']].values

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

        message = '**---- ข้อความจะถูกลบใน 60 วินาที ----**\n'
        message2 = ''

        for i,data in enumerate(databoard):
            # if str(1065206597833461850) in data
            if str(inter.author.id) in data:
                # scoreIndex = np.argwhere(scoreboard == str(inter.author.id))
                # accountIndex = np.argwhere(accountboard == str(inter.author.id))
                # email = accountboard[accountIndex[0][0]]
                message2 += f'\n**Bootcamp ID**: {data[1]} \n**Email**: {accountboard[i][1]} \n**Technical Preflop App Password**: {accountboard[i][2]} \n**คะแนนรวม**: {scoreboard[i][1]}'
        if not message2:
            message += '\n**Not found your id in database**'
        else:
            message += message2
        await inter.send(content=message, delete_after=60.0)
        print('Access profile successfully')



        


def setup(bot) -> None:
    """ Bind this cog to the bot """
    bot.add_cog(Request(bot))

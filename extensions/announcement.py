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
    async def request_key(
        self,
        inter:disnake.ApplicationCommandInteraction,
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
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='total_score!A:D').execute()
            rows = result.get('values', [])

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
        df = pd.DataFrame(rows[1:],columns=rows[0])
        
        temp_board = df.sort_values(by=['sum_point'],axis=0,ascending=False)
        board = temp_board[['Discord_id','sum_point']].values.tolist()
        
        guild_id = inter.guild_id
        guild = self.bot.get_guild(guild_id)
        
        name = []
        message = f'**Top 10 highest score**'
        for i in range(10):
            member = guild.get_member(int(board[i][0]))
            name.append(member.name + '#' + member.discriminator)
        for i in range(10):
            message += f"\n{name[i]} with score {board[i][1]}"
        await inter.send(content=message)
        # message = '**Message will be delete in 30 seconds**'
        
        # for i in rows:
        #         message += f'\nYour Bootcamp id is: {i[1]} \nYour java-app password is {i[2]} \n'
        # if not message:
        #     message += '\nNot found your id in database'
        # await inter.send(content=message,delete_after=30.0)
        
        # print(f"{user.id}"
        
    
    # @request_key.autocomplete("key_of")
    # async def key_autocomp(inter: disnake.ApplicationCommandInteraction, user_input: str):
    #     KEY_OF = ("bootcamp","java-app")
    #     return [ key
    #         for key in KEY_OF
    #         if user_input.lower() in key.lower()
    #     ]
        
    
def setup(bot) -> None:
	""" Bind this cog to the bot """
	bot.add_cog(Announcement(bot))
 
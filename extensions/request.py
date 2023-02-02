import disnake
from disnake.ext import commands

import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Request(commands.Cog):
    """ give a password for bootcamp or Java-app """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.cooldown(1, 1)
    @commands.dm_only()
    @commands.default_member_permissions(manage_guild=True, moderate_members=True)
    @commands.slash_command(name='profile',
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
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='info!A2:AB').execute()
            scoreResult = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='total_score!A2:B').execute()
            accountResult = service.spreadsheets().values().get(
                spreadsheetId=self.bot.config['googlesheet']['main_sheet'], range='preflop_account!A2:C').execute()
            datarows = dataResult.get('values', [])
            scorerows = scoreResult.get('values', [])
            accountrows = accountResult.get('values',[])

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

        message = '**ข้อความจะถูกลบใน 60 วินาที**\n'

        for i,data in enumerate(datarows):
            if str(inter.author.id) in data:
                message += f'\n**Bootcamp ID**: {data[0]} \n**Email**: {data[11]} \n**Technical Preflop App Password**: {accountrows[i][2]} \n**คะแนนรวม**: {scorerows[i][1]}'
        if not message:
            message += '\nNot found your id in database'
        await inter.send(content=message, delete_after=60.0)

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
    bot.add_cog(Request(bot))

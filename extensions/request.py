import disnake
from disnake.ext import commands

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Request(commands.Cog):
    """ give a password for bootcamp or Java-app """
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.cooldown(1,1)
    @commands.command(name = 'profile',
                            description= 'Get password for bootcamp website')
    async def request_key(
        inter:disnake.ApplicationCommandInteraction,
        # key_of:str
        
    ):
        """
        Sending back password to author

        Args:
            inter (disnake.GuildCommandInteraction): _description_
        """

        BC_COL = ''
        JAVA_COL = ''
        
        creds, _ = google.auth.default()
        # pylint: disable=maybe-no-member
        try:
            service = build('sheets', 'v4', credentials=creds)

            result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            rows = result.get('values', [])
            print(f"{len(rows)} rows retrieved")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
        await inter.send(content=message,delete_after=30.0)
        
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
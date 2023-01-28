import disnake
from disnake.ext import commands

class Request(commands.Cog):
    """ give a password for bootcamp or Java-app """
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.cooldown(1,1)
    @commands.slash_command(name = 'bootcamp',
                            description= 'Get password for bootcamp website')
    async def request_key(
        inter:disnake.ApplicationCommandInteraction,
        key_of:str
        
    ):
        """
        Sending back password to author

        Args:
            inter (disnake.GuildCommandInteraction): _description_
        """

        message = 'hello'
        await inter.send(content=message,delete_after=30.0)
        
        # print(f"{user.id}"
        
    
    @request_key.autocomplete("key_of")
    async def key_autocomp(inter: disnake.ApplicationCommandInteraction, user_input: str):
        KEY_OF = ("bootcamp","java-app")
        return [ key
            for key in KEY_OF
            if user_input.lower() in key.lower()
        ]
        
    

	
def setup(bot) -> None:
	""" Bind this cog to the bot """
	bot.add_cog(Request(bot))
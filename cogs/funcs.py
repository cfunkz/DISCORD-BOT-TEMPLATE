import discord
from discord.ext import commands

class Funcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        print(f'{__class__.__name__} cog unloaded')        

async def setup(bot):
    await bot.add_cog(Funcs(bot))
import discord
from discord.ext import commands
from database.functions import User
import logging

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def cog_load(self):
        return logging.info(f'{__class__.__name__} cog loaded')
    
    @commands.Cog.listener()
    async def on_interaction(self, message):
        if message.guild is None:
            return
        if message.user.bot:
            return
        User.add_xp(message.user.id, 10)
        
    def cog_unload(self):
        print(f'{__class__.__name__} cog unloaded')
        
async def setup(bot):
    await bot.add_cog(Events(bot))
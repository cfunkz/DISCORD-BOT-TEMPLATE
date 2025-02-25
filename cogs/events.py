import discord
from discord.ext import commands
from database.functions import User

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_interaction(self, message):
        if message.guild is None:
            return
        if message.user.bot:
            return
        User.add_xp(message.user.id, 10)
        
async def setup(bot):
    await bot.add_cog(Events(bot))
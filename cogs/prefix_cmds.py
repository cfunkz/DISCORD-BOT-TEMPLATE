from discord.ext import commands

# Prefix commands are called via "!" or any other prefix you set on the bot startup via bot.py

class PrefixCMDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Prefix commands uses "@commands" decorator.
    @commands.command(name="prefix", description="This is purely prefix command.")
    async def _ping_prefix(self, ctx):
        await ctx.send("I am a prefix command!")

    def cog_unload(self):
        print(f'{__class__.__name__} cog unloaded')
 
async def setup(bot):
    await bot.add_cog(PrefixCMDS(bot))
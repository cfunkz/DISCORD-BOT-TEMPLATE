from discord.ext import commands

# Hybrid commands are app_commands + prefix commands, but only ctx can be used. No Interaction object can be used.
# Hybrid commands are useful for when you want to use both app commands and prefix commands in the same command.

class HybridCMDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Hybrid commands uses "@commands" decorator.
    @commands.hybrid_command(name="ping", description="Pong!")
    async def _ping_hybrid_ctx(self, ctx):
        await ctx.send("Pong!")    

    def cog_unload(self):
        self.background_task.cancel()
        print(f'{__class__.__name__} cog unloaded')

async def setup(bot):
    await bot.add_cog(HybridCMDS(bot))
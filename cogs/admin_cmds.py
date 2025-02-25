from discord.ext import commands
from bot import ADMIN_IDS
from discord import Interaction
from discord.app_commands import command, Choice
import logging as logger

class AdminCMDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Hot-reload cogs
    @command(name="reload", description="Reload a cog")
    async def _reload_cog_interaction(self, interaction: Interaction, cog: str):
        if interaction.user.id not in ADMIN_IDS:
            return await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        if cog in self.bot.cogs:
            self.bot.reload_extension(f'cogs.{cog}')
            try:
                await self.bot.tree.sync()
            except Exception as e:
                await interaction.response.send_message(f'❌ {cog} cog failed to reload.', ephemeral=True)
                return logger.error(f'Error: {e}')
            await interaction.response.send_message(f'✅ {cog} cog reloaded.', ephemeral=True)
        else:
            await interaction.response.send_message(f'❌ {cog} cog not found.', ephemeral=True)

    @_reload_cog_interaction.autocomplete(name="cog")
    async def cog_autocomplete(
        self, interaction: Interaction, current: str
    ) -> list[Choice[str]]:
        """Autocompletes available cogs for the command."""
        return [
            Choice(name=cog, value=cog)
            for cog in self.bot.cogs.keys()
            if current.lower() in cog.lower()
        ]

    def cog_unload(self):
        print(f'{__class__.__name__} cog unloaded')

async def setup(bot):
    await bot.add_cog(AdminCMDS(bot))

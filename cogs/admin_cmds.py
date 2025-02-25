import os
from discord.ext import commands
from config import ADMIN_IDS, ADMIN_GUILDS
from discord import Interaction
from discord.app_commands import command, Choice, Group
import logging as logger

class AdminCMDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    inventory = Group(name="admin", description="Admin stuff!", guild_ids=ADMIN_GUILDS)

    @command(name="reload", description="Reload a cog")
    async def _reload_cog_interaction(self, interaction: Interaction, cog: str):
        if interaction.user.id not in ADMIN_IDS:
            return await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        cog_path = f'cogs.{cog}'
        if cog_path not in self.bot.extensions:
            return await interaction.response.send_message(f'❌ {cog} cog is not loaded.', ephemeral=True)
        try:
            await self.bot.reload_extension(cog_path)
            await interaction.response.send_message(f'✅ {cog} cog reloaded.', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'❌ {cog} cog failed to reload.', ephemeral=True)
            logger.error(f'Error: {e}')

    @_reload_cog_interaction.autocomplete(name="cog")
    async def cog_autocomplete(self, interaction: Interaction, current: str) -> list[Choice[str]]:
        """Autocompletes available cogs from the 'cogs' folder."""
        cogs = [
            f[:-3] for f in os.listdir("cogs")
            if f.endswith(".py") and f != "__init__.py"
        ]

        return [
            Choice(name=cog, value=cog)
            for cog in cogs
            if current.lower() in cog.lower()
        ]

    def cog_unload(self):
        print(f'{__class__.__name__} cog unloaded')
    def cog_load(self):
        return logger.info(f'{__class__.__name__} cog loaded')

async def setup(bot):
    await bot.add_cog(AdminCMDS(bot))

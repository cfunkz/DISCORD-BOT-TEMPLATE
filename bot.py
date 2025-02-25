import discord
from discord import app_commands
from discord.ext import commands
import logging, os
from utils import get_time
from dotenv import load_dotenv
from database import init_db

load_dotenv()

TOKEN=os.getenv('TOKEN')
ADMIN_IDS=os.getenv('ADMIN_IDS')
ADMIN_GUILDS = os.getenv('ADMIN_GUILDS')
OWNER = os.getenv('OWNER')

logging.basicConfig(level=logging.INFO)  # Suppress messages below ERROR level
logger = logging.getLogger(__name__)

class MainBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, owner_ids=OWNER, activity=discord.Game(name="THIS IS A SAMPLE MESSAGE AS ACTIVITY"))
        
    async def setup_hook(self):
        await self.load_cogs()
        logger.info(' Cogs loaded')
        init_db()
        logger.info(' Database initialized')
        logger.info(' Setup hook done.')

    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Cog {filename[:-3]} loaded')

    async def on_ready(self):
        #clear_old_commands = self.tree.clear_commands(guild=None)
        #if clear_old_commands:
            #print("Old app commands cleared...")
        synced = await self.tree.sync()
        amount = len(synced) if synced else 0
        logger.info(f"###### Bot ready! Synced Commands: {amount} ######")
        print(f'Logged in as {self.user.name}')
        
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required command argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad command argument provided.")
        elif isinstance(error, commands.CommandOnCooldown):
            hours, minutes, seconds = get_time(error)
            if hours > 0:
                cooldown_message = f"This command is on cooldown. Try again in {hours:.0f} hours and {minutes:.0f} minutes."
            elif minutes > 0:
                cooldown_message = f"This command is on cooldown. Try again in {minutes:.0f} minutes."
            else:
                cooldown_message = f"This command is on cooldown. Try again in {seconds:.0f} seconds."
            embed = discord.Embed(title="Command on Cooldown", description=cooldown_message, color=discord.Color.red())
            embed.set_thumbnail(url="https://emojicdn.elk.sh/⏰")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, app_commands.CommandInvokeError):
            original_error = getattr(error, "original", error)
            await ctx.send(f"An error occurred: {original_error}")
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f"Failed to send a message due to missing permissions in channel: {ctx.channel.id}")
        else:
            await ctx.send(f"An error occurred while executing the command.\n```{error}```")

intents = discord.Intents.default()
intents.guilds = True # Get guild information
intents.message_content = True # For prefix commands
intents.presences = True # For presence intents

client = MainBot(intents=intents)

if __name__ == '__main__':
    client.run(TOKEN)
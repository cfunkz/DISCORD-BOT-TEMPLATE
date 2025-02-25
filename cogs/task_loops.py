import discord
from discord.ext import commands, tasks
import random
import logging

class TaskLoops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.texts = ['Text1 will change in 30sec', 'Text2 will change in 30sec', 'Text3 will change in 30sec']
        self.background_task.start()

    # Task loops can be run x hours, minutes, seconds, etc.
    # This task loop will change the bot's presence status every 30 seconds.
    @tasks.loop(seconds=30)
    async def background_task(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Game(name=random.choice(self.texts)))
    
    def cog_unload(self):
        self.background_task.cancel()
        print(f'{__class__.__name__} cog unloaded')
    def cog_load(self):
        return logging.info(f'{__class__.__name__} cog loaded')

async def setup(bot):
    await bot.add_cog(TaskLoops(bot))
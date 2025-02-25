from discord.ui import Select
import discord

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Option 1",emoji="👌",description="This is option 1!"),
            discord.SelectOption(label="Option 2",emoji="✨",description="This is option 2!"),
            discord.SelectOption(label="Option 3",emoji="🎭",description="This is option 3!")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Your choice is {self.values[0]}!",ephemeral=True)

class SelectMenuView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=None)
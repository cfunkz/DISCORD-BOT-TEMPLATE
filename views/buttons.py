from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import discord

class ButtonView(View):
    def __init__(self, user):
        super().__init__(timeout=30)
        self.user = user
        
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit_message(view=None)
            self.stop()
            
    @discord.ui.button(emoji="👍", label="Click Me!", row=1, style=discord.ButtonStyle.primary)
    async def button_1(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.id == self.user.id:
            return await interaction.response.send_message(f"{interaction.user.name} is not allowed to click this button! Only {self.user.name}")
        await interaction.response.send_message("You clicked the button!")
        
    @discord.ui.button(emoji="💻", label="Server", row=2, style=discord.ButtonStyle.primary)
    async def button_2(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.id == self.user.id:
            return await interaction.response.send_message(f"{interaction.user.name} is not allowed to click this button! Only {self.user.name}")
        await interaction.response.send_message(f"You are in {interaction.guild.name}!")

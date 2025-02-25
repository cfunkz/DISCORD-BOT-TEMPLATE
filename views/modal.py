import discord
from discord.ui import Modal, TextInput

class MyModal(Modal):
    def __init__(self):
        super().__init__(title="Modal test")
        self.text_input = TextInput(label="Your input:", style=discord.TextStyle.short)
        self.add_item(self.text_input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You entered: {self.text_input.value}")
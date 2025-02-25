import discord
from discord.ext import commands
from discord import Interaction, Member
from discord.app_commands import Choice, command, describe, choices, Group
from typing import Literal
from database.functions import User
import json
from views.modal import MyModal
from views.selectmenu import SelectMenuView
from views.buttons import ButtonView
import logging
# Slash commands or app_commands that are used via "/"

class SlashCMDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash commands uses "@app_commands" decorator.
    @command(name="start", description="Create a user profile!")
    async def _start(self, inter: Interaction):
        User.add_user(inter.user.id)
        await inter.response.send_message("User profile created!", ephemeral=True)

    @command(name="profile", description="Get detailed profile information!")
    async def _get_profile(self, inter: Interaction):
        member = inter.user
        embed = discord.Embed(title=f"Profile of {member.name}#{member.discriminator}", color=discord.Color.blue())
        embed.add_field(name="Username", value=f"{member.global_name}#{member.discriminator}", inline=False)
        embed.add_field(name="Display Name", value=member.display_name, inline=False)
        embed.add_field(name="Mention", value=member.mention, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Status", value=str(member.status), inline=False)
        embed.add_field(name="Top Role", value=member.top_role.name, inline=False)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%b %d, %Y, %H:%M:%S"), inline=False)
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%b %d, %Y, %H:%M:%S"), inline=False)
        # Roles
        if len(member.roles) > 1:
            roles = [role.name for role in member.roles[1:]]  # Exclude @everyone role
            embed.add_field(name="Roles", value=", ".join(roles), inline=False)
        else:
            embed.add_field(name="Roles", value="No roles", inline=False)
        # Avatar
        embed.set_thumbnail(url=member.avatar.url if member.avatar else "https://cdn.discordapp.com/embed/avatars/0.png")
        await inter.response.send_message(embed=embed, ephemeral=True)

    @command(name="user", description="Get a user profile summary!")
    async def _get_user(self, inter: Interaction, member: Member):
        embed = discord.Embed(title=f"User Info: {member.global_name}#{member.discriminator}", color=discord.Color.green())
        embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=False)
        embed.add_field(name="Display Name", value=member.display_name, inline=False)
        embed.add_field(name="Mention", value=member.mention, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Join Date", value=member.joined_at.strftime("%b %d, %Y"), inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%b %d, %Y"), inline=False)
        embed.add_field(name="Status", value=str(member.status), inline=False)
        if len(member.roles) > 1:
            roles = [role.name for role in member.roles[1:]]  # Exclude @everyone role
            embed.add_field(name="Roles", value=", ".join(roles), inline=False)
        else:
            embed.add_field(name="Roles", value="No roles", inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else "https://cdn.discordapp.com/embed/avatars/0.png")
        await inter.response.send_message(embed=embed, ephemeral=True)
    
    
    ############### Command options
    @command(name="literal_options", description="Get server information!")
    async def _literal_options(self, inter: Interaction, option: Literal["option1", "option2", "option3"]):
        await inter.response.send_message(f"Option selected: {option}", ephemeral=True)
        
    ############### Command options 2
    @command(name="app_command_options", description="Get server information!")
    @describe(option="Choose an option")
    @choices(
        option=[
            Choice(name="Option 1", value="option1"),
            Choice(name="Option 2", value="option2"),
            Choice(name="Option 3", value="option3")
        ]
    )
    async def _app_command_options(self, inter: Interaction, option: Choice[str]):
        await inter.response.send_message(f"Option selected: {option.name}", ephemeral=True)

    ############### Command with modal
    @command(name="modal", description="Modal test!")
    async def _modal_hybrid_ctx(self, inter: Interaction):
        await inter.response.send_modal(MyModal())

    ############### Command with select menu
    @command(name="selectmenu", description="Example of Select Menu")
    async def select_menu_command(self, interaction: discord.Interaction):
        view = SelectMenuView()
        await interaction.response.send_message("Please select an option from the menu:", view=view)
        message = await interaction.original_response()
        view.message = message #Attach message to view
        
    ############### Command with buttons
    @command(name="buttons", description="Example of Buttons")
    async def button_command(self, inter: discord.Interaction):
        view = ButtonView(inter.user)
        await inter.response.send_message("Click a button:", view=view)
        message = await inter.original_response()
        view.message = message #Attach message to view
        
    ############### Command groups
    inventory = Group(name="inventory", description="Get user inventory!")

    @inventory.command(name="check", description="Check your inventory!")
    async def _get_inventory(self, inter: Interaction):
        user = User.get_user(inter.user.id)
        if user is None:
            await inter.response.send_message("Register via `/start`.", ephemeral=True)
        user_inventory = json.loads(user['inventory'])  # Load the inventory (from JSON)
        # Format inventory as a string
        inventory_str = '\n'.join([f"{item}: {amount}" for item, amount in user_inventory.items()])
        embed = discord.Embed(title=f"{inter.user.name}'s Inventory", color=discord.Color.gold())
        embed.add_field(name="Items", value=inventory_str if inventory_str else "No items!", inline=False)
        await inter.response.send_message(embed=embed, ephemeral=True)

    # Command to use an item (removes 1 from the inventory)
    @inventory.command(name="use", description="Use an item from your inventory!")
    async def _use_inventory(self, inter: Interaction, item: str):
        user = User.get_user(inter.user.id)
        if user is None:
            await inter.response.send_message("Register via `/start`.", ephemeral=True)
        user_inventory = json.loads(user['inventory'])  # Load the inventory (from JSON)
        if not user_inventory:
            await inter.response.send_message("Register via `/start`.", ephemeral=True)
        # Check if item exists in inventory
        if item in user_inventory and user_inventory[item] > 0:
            user_inventory[item] -= 1
            # If the amount reaches 0, remove the item from the inventory
            if user_inventory[item] == 0:
                del user_inventory[item]
            # Update the inventory in the database
            new_inventory = json.dumps(user_inventory)
            User.update_inventory(inter.user.id, new_inventory)
            await inter.response.send_message(f"Used 1 {item}. You now have {user_inventory.get(item, 0)} left.", ephemeral=True)
        else:
            await inter.response.send_message(f"You don't have any {item} in your inventory.", ephemeral=True)

    # Autocomplete for the `use` command, `item` argument
    @_use_inventory.autocomplete('item')
    async def search_autocomplete(self, interaction: discord.Interaction, item: str):
        user = User.get_user(interaction.user.id)
        if user is None:
            return []
        user_inventory = json.loads(user['inventory'])  # Load the inventory (from JSON)
        # Filter items based on the user input
        matching_items = [i for i in user_inventory if item.lower() in i.lower()]
        # Return filtered matching items as autocompletion choices
        return [Choice(name=i, value=i) for i in matching_items]
    
    def cog_unload(self):
        print(f'{__class__.__name__} cog unloaded')
    
    def cog_load(self):
        return logging.info(f'{__class__.__name__} cog loaded')
    
async def setup(bot):
    await bot.add_cog(SlashCMDS(bot))
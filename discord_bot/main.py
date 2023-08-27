# bot.py
import os

import discord
from dotenv import load_dotenv
from random import random
from discord import app_commands
from server_connector import ServerConnector

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
AUTHAURIZED_USER = [int(x) for x in os.getenv('DISCORD_AUTHORIZED_USER').split(',')]
REST_BEARER_TOKEN = os.getenv('REST_BEARER_TOKEN')

intents = discord.Intents.all()

client = discord.Client(command_prefix='!', intents=intents)
tree = app_commands.CommandTree(client)


server_connection = ServerConnector("minecraft.hexadecilab.com", 8080, REST_BEARER_TOKEN)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

 # if slash command isn't in a cog
@tree.command(name = "commandname", description = "My first application Command", guild=discord.Object(id=GUILD_ID)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction: discord.Interaction):
    if interaction.user.id not in AUTHAURIZED_USER:
        print(f"{interaction.user.name} tried to use the command but is not authorized."
              f"({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    await interaction.response.send_message("Hello!")
    
class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Send Message', style=discord.ButtonStyle.green)
    async def send_message(self,  interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_message('Hello World!', ephemeral=False)


class MenuStop(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Stop Server', style=discord.ButtonStyle.red)
    async def stop_server(self,  interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_message('Hello World!', ephemeral=False)






@tree.command(name = "buttoncommand", description = "My first button Command", guild=discord.Object(id=GUILD_ID))
async def button_command(interaction: discord.Interaction):
    if interaction.user.id not in AUTHAURIZED_USER:
        print(f"{interaction.user.name} tried to use the command but is not authorized."
              f"({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    await interaction.response.send_message("Hello!", view=Menu(),ephemeral=True)


@tree.command(name = "serverstatus", description = "Display the status of the server", guild=discord.Object(id=GUILD_ID))
async def server_status(interaction: discord.Interaction):
    result = server_connection.get_server_status()
    
    # create embed
    
    embed = discord.Embed(title="Server Status", description="The server is currently " + ("running" if result else "not running"), color=0x00ff00 if result else 0xff0000)
    embed.set_footer(text="HexadeciLab")
    
    await interaction.response.send_message(embed=embed, ephemeral=False)

@tree.command(name = "serverlogs", description = "Display the logs of the server", guild=discord.Object(id=GUILD_ID))
async def server_logs(interaction: discord.Interaction):
    
    result = server_connection.get_server_logs()
    
    # create embed
    
    embed = discord.Embed(title="Server Logs", description=result, color=0x00ff00 if result else 0xff0000)
    embed.set_footer(text="HexadeciLab")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(TOKEN)
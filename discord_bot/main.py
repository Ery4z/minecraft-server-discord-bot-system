# bot.py
import os

import discord
from dotenv import load_dotenv
from random import random
from discord import app_commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
AUTHAURIZED_USER = [int(x) for x in os.getenv('DISCORD_AUTHORIZED_USER').split(',')]
REST_BEARER_TOKEN = os.getenv('REST_BEARER_TOKEN')

intents = discord.Intents.all()

client = discord.Client(command_prefix='!', intents=intents)
tree = app_commands.CommandTree(client)




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

client.run(TOKEN)
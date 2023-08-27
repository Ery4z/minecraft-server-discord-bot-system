# bot.py
import os

import discord
from dotenv import load_dotenv
from random import random
from discord import app_commands
from server_connector import ServerConnector
import nmap

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
AUTHAURIZED_USER = [int(x) for x in os.getenv('DISCORD_AUTHORIZED_USER').split(',')]
REST_BEARER_TOKEN = os.getenv('BACKDOOR_BEARER_TOKEN')
SERVER_IP = os.getenv('BACKDOOR_IP')
BACKDOOR_PORT = os.getenv('BACKDOOR_PORT')

nm = nmap.PortScanner()


intents = discord.Intents.all()

client = discord.Client(command_prefix='!', intents=intents)
tree = app_commands.CommandTree(client)

server_connection = ServerConnector(SERVER_IP, BACKDOOR_PORT, REST_BEARER_TOKEN)

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



class MenuServerControlStopped(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Start Server', style=discord.ButtonStyle.green)
    async def start_server(self,  interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        server_result = server_connection.post_start_server()
        
        embed = discord.Embed(title="Server Status", description=("The server has been started!" if server_result else "An error occured, the server has not been started. Check the logs."), color=0x00ff00 if server_result else 0xff0000)
        if server_result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")

            await interaction.followup.send(embed=embed, ephemeral=False)
        else:
            embed.set_thumbnail(url="https://31.media.tumblr.com/95c8b33f188c0e50a886a4492bfa3e39/tumblr_myhni5WwBC1s5nggto1_250.gif")
            await interaction.followup.send(embed=embed, ephemeral=True)


class MenuServerControlStarted(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Stop Server', style=discord.ButtonStyle.red)
    async def stop_server(self,  interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        server_result = server_connection.post_stop_server()
        
        embed = discord.Embed(title="Server Status", description=("The server has been stopped!" if server_result else "An error occured, the server has not been stopped. Check the logs."), color=0x00ff00 if server_result else 0xff0000)
        if server_result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")
            await interaction.followup.send(embed=embed, ephemeral=False)
        else:
            embed.set_thumbnail(url="https://31.media.tumblr.com/95c8b33f188c0e50a886a4492bfa3e39/tumblr_myhni5WwBC1s5nggto1_250.gif")
            
            await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(label='Restart Server', style=discord.ButtonStyle.blurple)
    async def restart_server(self,  interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        server_result = server_connection.post_restart_server()
        
        embed = discord.Embed(title="Server Status", description=("The server is restarting..." if server_result else "An error occured, the server has not been restarted. Check the logs."), color=0x00ff00 if server_result else 0xff0000)
        if server_result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")

            await interaction.followup.send(embed=embed, ephemeral=False)
        else:
            await interaction.followup.send(embed=embed, ephemeral=True)

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
    
    await interaction.response.defer(ephemeral=False)
    result = server_connection.get_server_status()
    
    nm.scan(SERVER_IP,'25565')
    ip = nm.all_hosts()[0]
    networkStatus = nm[ip]['tcp'][25565]['state'] == 'open'
    
    
    # create embed
    
    embed = discord.Embed(title="Server Status", description="The server is currently " + ("running" if result else "not running"), color=0x00ff00 if result else 0xff0000)
    if networkStatus:
        player_count = nm[ip]['tcp'][25565]['extrainfo'].split('Users: ')[1].split("'")[0]
        embed.add_field(name="", value=player_count+" players connected")
    if result:
        embed.set_thumbnail(url="https://i.gifer.com/D00b.gif")
    else:
        embed.set_thumbnail(url="https://media.tenor.com/tMNK4LEnFlMAAAAC/sheep-fuck.gif")
    
    
    embed.set_footer(text="HexadeciLab")
    
    await interaction.followup.send(embed=embed, ephemeral=False)

@tree.command(name = "serverlogs", description = "Display the logs of the server", guild=discord.Object(id=GUILD_ID))
async def server_logs(interaction: discord.Interaction):
    
    await interaction.response.defer(ephemeral=True)
    
    result = server_connection.get_server_logs()
    
    # create embed
    
    embed = discord.Embed(title="Server Logs", description=result, color=0x00ff00 if result else 0xff0000)
    embed.set_footer(text="HexadeciLab")
    
    await interaction.followup.send(embed=embed, ephemeral=True)
    
@tree.command(name = "servercontrol", description = "Control the server", guild=discord.Object(id=GUILD_ID))
async def server_control(interaction: discord.Interaction):
    if interaction.user.id not in AUTHAURIZED_USER:
        print(f"{interaction.user.name} tried to use the command but is not authorized."
              f"({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    
    serverStatus = server_connection.get_server_status()
    nm.scan(SERVER_IP,'25565')
    ip = nm.all_hosts()[0]
    networkStatus = nm[ip]['tcp'][25565]['state'] == 'open'
    embed=discord.Embed(title="Server Control")
    embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/002/187/715/02a.gif")
    embed.add_field(name="Service", value="The service is currently "+("ON ✅" if serverStatus else "OFF ❌") , inline=True)
    embed.add_field(name="Network Firewall", value="The server is currently" +(" reacheable ✅" if networkStatus else " not reacheable ❌"), inline=False)
    embed.set_footer(text="Micro Informatique Service Bot")
    if serverStatus:
        await interaction.followup.send(embed=embed, view=MenuServerControlStarted(),ephemeral=True)
    else:
        await interaction.followup.send(embed=embed, view=MenuServerControlStopped(),ephemeral=True)

client.run(TOKEN)
# bot.py
import os

import discord
from dotenv import load_dotenv
from random import random
from discord import app_commands
from server_connector import ServerConnector
from oracle_connector import OracleConnector
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD')
AUTHAURIZED_USER = [int(x) for x in os.getenv('DISCORD_AUTHORIZED_USER').split(',')]
REST_BEARER_TOKEN = os.getenv('BACKDOOR_BEARER_TOKEN')
SERVER_IP = os.getenv('BACKDOOR_IP')
BACKDOOR_PORT = os.getenv('BACKDOOR_PORT')

ORACLE_AUTH_TOKEN = os.getenv('ORACLE_AUTH_TOKEN')
ORACLE_SUBNET = os.getenv('ORACLE_SUBNET')

intents = discord.Intents.all()

client = discord.Client(command_prefix='!', intents=intents)
tree = app_commands.CommandTree(client)

oracle = OracleConnector(ORACLE_AUTH_TOKEN, ORACLE_SUBNET)
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
        
        server_result = server_connection.start_server()
        
        embed = discord.Embed(title="Server Status", description=("The server has been started!" if server_result else "An error occured, the server has not been started. Check the logs."), color=0x00ff00 if server_result else 0xff0000)
        if server_result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")

            await interaction.response.send_message(embed, ephemeral=False)
        else:
            embed.set_thumbnail(url="https://31.media.tumblr.com/95c8b33f188c0e50a886a4492bfa3e39/tumblr_myhni5WwBC1s5nggto1_250.gif")
            await interaction.response.send_message(embed, ephemeral=True)


class MenuServerControlStarted(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Stop Server', style=discord.ButtonStyle.red)
    async def stop_server(self,  interaction: discord.Interaction,button: discord.ui.Button):
        
        server_result = server_connection.stop_server()
        
        embed = discord.Embed(title="Server Status", description=("The server has been stopped!" if server_result else "An error occured, the server has not been stopped. Check the logs."), color=0x00ff00 if server_result else 0xff0000)
        if server_result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")
            await interaction.response.send_message(embed, ephemeral=False)
        else:
            embed.set_thumbnail(url="https://31.media.tumblr.com/95c8b33f188c0e50a886a4492bfa3e39/tumblr_myhni5WwBC1s5nggto1_250.gif")
            
            await interaction.response.send_message(embed, ephemeral=True)

    @discord.ui.button(label='Restart Server', style=discord.ButtonStyle.Blue)
    async def restart_server(self,  interaction: discord.Interaction,button: discord.ui.Button):
        
        server_result = server_connection.restart_server()
        
        embed = discord.Embed(title="Server Status", description=("The server is restarting..." if server_result else "An error occured, the server has not been restarted. Check the logs."), color=0x00ff00 if server_result else 0xff0000)
        if server_result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")

            await interaction.response.send_message(embed, ephemeral=False)
        else:
            await interaction.response.send_message(embed, ephemeral=True)

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
    
@tree.command(name = "servercontrol", description = "Control the server", guild=discord.Object(id=GUILD_ID))
async def server_control(interaction: discord.Interaction):
    if interaction.user.id not in AUTHAURIZED_USER:
        print(f"{interaction.user.name} tried to use the command but is not authorized."
              f"({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    
    serverStatus = server_connection.get_server_status()
    networkStatus = True#server_connection.get_network_status() 
    
    embed=discord.Embed(title="Server Control")
    embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/002/187/715/02a.gif")
    embed.add_field(name="Service", value="The service is currently "+("ON ✅" if serverStatus else "OFF ❌") , inline=True)
    embed.add_field(name="Network Firewall", value="The server is currently" +(" reacheable ✅" if networkStatus else " not reacheable ❌"), inline=False)
    embed.set_footer(text="Micro Informatique Service Bot")
    if serverStatus:
        await interaction.response.send_message("The server is running!", view=MenuServerControlStarted(),ephemeral=True)


@tree.command(name = "netaddips", description = "Add ip to the network firewall", guild=discord.Object(id=GUILD_ID))
async def server_logs(interaction: discord.Interaction, ips: str):
    
    # Prevent to run the command if the environment variable is not set
    to_verify = [ORACLE_AUTH_TOKEN, ORACLE_SUBNET]
    for var in to_verify:
        if var is None:
            await interaction.response.send_message("The environment variable " + var + " is not set.", ephemeral=True)
            return
        if var == "":
            await interaction.response.send_message("The environment variable " + var + " is empty.", ephemeral=True)
            return
        
    if interaction.user.id not in AUTHAURIZED_USER:
        print(f"{interaction.user.name} tried to use the command but is not authorized."
              f"({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    
    ips = ips.split(',')
    res = oracle.set_allowed_ips(ips)
    if res :
        embed = discord.Embed(title="Network Firewall", description="The ips have been added to the firewall", color=0x00ff00)
        embed.set_footer(text="HexadeciLab")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Network Firewall", description="An error occured, the ips have not been added to the firewall", color=0xff0000)
        embed.set_footer(text="HexadeciLab")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class MenuNetworkControl(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Allow Everyone', style=discord.ButtonStyle.green)
    async def allow_everyone(self,  interaction: discord.Interaction,button: discord.ui.Button):
        
        result = oracle.set_allow_all()
        
        embed = discord.Embed(title="Network Status", description=("The server is now reachable!" if server_result else "An error occured."), color=0x00ff00 if server_result else 0xff0000)
        if result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")
            await interaction.response.send_message(embed, ephemeral=False)
        else:
            embed.set_thumbnail(url="https://31.media.tumblr.com/95c8b33f188c0e50a886a4492bfa3e39/tumblr_myhni5WwBC1s5nggto1_250.gif")
            await interaction.response.send_message(embed, ephemeral=True)

    @discord.ui.button(label='Block Everyone', style=discord.ButtonStyle.Blue)
    async def restart_server(self,  interaction: discord.Interaction,button: discord.ui.Button):
        
        result = oracle.delete_firewall_rules_by_port()
        
        embed = discord.Embed(title="Server Status", description=("The server access is now blocked to anyone." if server_result else "An error occured. Check the logs."), color=0x00ff00 if server_result else 0xff0000)
        if result:
            embed.set_thumbnail(url="https://gifdb.com/images/high/team-fortress-2-engineer-thumbs-up-i8g0444qxrmcwh9t.gif")

            await interaction.response.send_message(embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed, ephemeral=True)


@tree.command(name = "netcontrol", description = "Control Panel for the firewall", guild=discord.Object(id=GUILD_ID))
async def network_control(interaction: discord.Interaction):
    
    # Prevent to run the command if the environment variable is not set
    to_verify = [ORACLE_AUTH_TOKEN, ORACLE_SUBNET]
    for var in to_verify:
        if var is None:
            await interaction.response.send_message("The environment variable " + var + " is not set.", ephemeral=True)
            return
        if var == "":
            await interaction.response.send_message("The environment variable " + var + " is empty.", ephemeral=True)
            return
    
    
    
    if interaction.user.id not in AUTHAURIZED_USER:
        print(f"{interaction.user.name} tried to use the command but is not authorized."
              f"({interaction.user.id})")
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return
    
    allowed_ips = oracle.get_allowed_ips()
    embed=discord.Embed(title="Network Firewall Control Panel")
    embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/original/002/187/715/02a.gif")
    if "0.0.0.0/0" in allowed_ips:
        embed.add_field(name="Allowed IPs", value="The firewall is currently allowing all ips", inline=True)
    else :
        embed.add_field(name="Allowed IPs", value="The firewall is currently allowing the following ips : " + ", ".join(allowed_ips), inline=True)
    embed.set_footer(text="Micro Informatique Service Bot")

    await interaction.response.send_message(embed=embed, view=MenuNetworkControl(),ephemeral=True)

client.run(TOKEN)
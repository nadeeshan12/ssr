import discord
import datetime
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING
import dotenv
import os
import asyncio
import json
import pytz

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')

#---------------------------------------------Variables-------------------------
#Guilds
server_id = 1376872792242389012

#roles
admin_role_id = 1376872792309502003
staff_id = 1376872792276074535
whitelist_id = 1376872792309502004

#channels
whitelist_respond_id = 1376872792879796323
log_channel_id = 1376872792879796323
announcement_id = 1392741175018131517
user_info = 1391794200336531528

#colors
theme_color = 0x000000
green = 0x21b10a
red = 0xd62f31

#server_info
server_name = 'SouthSide Roleplay©'
application_team = 'SouthSide Roleplay Application Team'

#logo
server_logo = 'logo.png'

#admin-logs
respond_log_id = 1376872793890754614
whitelist_log_id = 1376872793890754614
banned_log_id = 1376872793890754614

#------------------------------------------------Base----------------------------
class abot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = '?', intents = discord.Intents.all())
        self.synced = False
        
    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=server_id))
        self.synced = True
        print('Bot is ready')
        
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send('`Bot is Stating Up 🔃`')
        
        while True:
            members_count = bot.get_guild(server_id).member_count
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='SouthSide Roleplay'))
            await asyncio.sleep(10.0)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{members_count} Members'))
            await asyncio.sleep(10.0)

bot = abot()
tree = bot.tree

async def main():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    await bot.start(TOKEN)

#----------------------------------------------Design------------------------------
class GeneralForum(discord.ui.Modal, title = 'General Ticket'):
    try:
        ttl = discord.ui.TextInput(label='Your Problem', style=discord.TextStyle.short, placeholder='What is your problem?', required=True)
        des = discord.ui.TextInput(label='Description', style=discord.TextStyle.long, placeholder='Briefly Describe your problem', required=True)
    
        async def on_submit(self, interaction: discord.Interaction) -> None:
            await interaction.response.defer(ephemeral=True)
            member = interaction.user
            memid = member.id
            
            channel = discord.utils.get(interaction.guild.text_channels, name=f'ticket-{interaction.user.name}-{interaction.user.discriminator}')
            if channel is not None: await interaction.response.send_message("You already have an existing ticket", ephemeral=True)
            if channel is None:
                category =  discord.utils.get(interaction.guild.categories, name=f'General Tickets')
                if category is None:
                    category = await interaction.guild.create_category('General Tickets')
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                    interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
                    interaction.guild.me:discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
                }
                channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}-{interaction.user.discriminator}', overwrites=overwrites, category=category)
                await channel.send(f'# {self.ttl.value}')
                await channel.send(f'** {self.des.value} **')
                await channel.send(interaction.user.mention)
                await interaction.followup.send(f'Your Ticket has been created at {channel.mention}', ephemeral=True)
                
                channelid = str(channel.id)
                with open('ticket.json') as db:
                    data = json.load(db)
                
                    if not channelid in data:
                        data[channelid] = {
                            "id":memid,
                            "name":member.name,
                            "title":self.ttl.value,
                            "description":self.des.value
                        }
                    
                    with open('ticket.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    
                log_channel = bot.get_channel(log_channel_id)
                embed = discord.Embed(title='Ticked Opened', description=f'**Ticket** \n {channel.name} \n **Member**  \n {interaction.user.mention} ({interaction.user.id})')
                embed.timestamp = datetime.datetime.now()
                embed.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar.url}')
                embed.set_footer(text=server_name, icon_url=server_logo)
                embed.set_thumbnail(url=server_logo)
                await log_channel.send(embed=embed)
    except Exception as e:
        print(e)    

class SetupButton2(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.red, label='Player Report')
        
    async def callback(self, interaction: discord.Interaction):
        try:
            modal = ReportForum()
            await interaction.response.send_modal(modal)
        except Exception as e:
            print(e)
        
class ReportForum(discord.ui.Modal, title = 'Create a Player Report'):
    try:
        ttl = discord.ui.TextInput(label='Your Problem', style=discord.TextStyle.short, placeholder='What is your problem?', required=True)
        des = discord.ui.TextInput(label='Description', style=discord.TextStyle.long, placeholder='Briefly Describe your problem', required=True)
    
        async def on_submit(self, interaction: discord.Interaction) -> None:
            member = interaction.user
            memid = member.id
            
            channel = discord.utils.get(interaction.guild.text_channels, name=f'ticket-{interaction.user.name}-{interaction.user.discriminator}')
            if channel is not None: await interaction.response.send_message("You already have an existing ticket", ephemeral=True)
            if channel is None:
                category =  discord.utils.get(interaction.guild.categories, name=f'Player Reports')
                if category is None:
                    category = await interaction.guild.create_category('Player Reports')
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                    interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
                    interaction.guild.me:discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
                }
                channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}-{interaction.user.discriminator}', overwrites=overwrites, category=category)
                await channel.send(f'# {self.ttl.value}')
                await channel.send(f'** {self.des.value} **')
                await channel.send(interaction.user.mention)
                await interaction.response.send_message(f'You opened a ticked. visit {channel.mention}')
                await interaction.response.send_message(f'Your Ticket has been created at {channel.mention}', ephemeral=True)
                
                channelid = str(channel.id)
                with open('ticket.json') as db:
                    data = json.load(db)
                
                    if not channelid in data:
                        data[channelid] = {
                            "id":memid,
                            "name":member.name,
                            "title":self.ttl.value,
                            "description":self.des.value
                        }
                    
                    with open('ticket.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    
                log_channel = bot.get_channel(log_channel_id)
                embed = discord.Embed(title='Ticked Opened', description=f'**Ticket** \n {channel.name} \n **Member**  \n {interaction.user.mention} ({interaction.user.id})')
                embed.timestamp = datetime.datetime.now()
                embed.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar.url}')
                embed.set_footer(text=server_name, icon_url=server_logo)
                embed.set_thumbnail(url=server_logo)
                await log_channel.send(embed=embed)
    except Exception as e:
        print(e)    

class SetupButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.green, label='Create a Ticket')
        
    async def callback(self, interaction: discord.Interaction):
        try:
            modal = GeneralForum()
            await interaction.response.send_modal(modal)
        except Exception as e:
            print(e)

                
#---------------------------------------------Commands------------------------------
#============================================= Respond ==============================
@bot.command(name='rs')
@commands.has_any_role(staff_id, admin_role_id)
async def respond(ctx, memberid, result):
    try:
        member = ctx.guild.get_member(int(memberid))
        log_channel = bot.get_channel(log_channel_id)
        
        des = ''
        res = ''
        color = None
        if result == 'pass':
            des = f'Hi {member.mention}, Your Form Has Been Accepted ✅, Please Join For Voice Channel Contact the staff Interview Details.'
            res = 'Passed ✅'
            color = green
        elif result == 'fail':
            des = f'Hi {member.mention}, Unfortunately your application has been Rejected ❌. Feel free to reapply'
            res = 'Failed ❌'
            color = red
        else:
            ctx.send("Result must be pass or fail")
        
        rs_embed = discord.Embed(color=color, title='Whitelist Application Respond', description=des)
        rs_embed.timestamp = datetime.datetime.now()
        rs_embed.set_author(name=application_team)
        rs_embed.set_footer(text=server_name, icon_url=server_logo)
        rs_embed.set_thumbnail(url=server_logo)
        rs_embed.add_field(name='Result', value=res)
        
        DMChannel = await member.create_dm()
        try:
            await DMChannel.send(embed=rs_embed)
            await log_channel.send(f'`{member.name} has recieved DM Successfully ✅`')
        except discord.Forbidden:
            await log_channel.send(f'`{member.name} has not recieved DM ❌`')
        except discord.HTTPException:
            await log_channel.send(f'`{member.name} has not recieved DM ❌`')
        
    
        with open('responds.json') as file:
            data = json.load(file)
        
            data[memberid] = {
                "memberid":memberid,
                "membername":member.name,
                "approved":ctx.author.name,
                "result":res
            }
            with open('responds.json', 'w') as f:
                json.dump(data,f,indent=4)
    
        whitelist_respond = bot.get_channel(whitelist_respond_id)
        await whitelist_respond.send(embed=rs_embed)
        await ctx.message.delete()
    
        
        admin_log = bot.get_channel(respond_log_id)
        embed = discord.Embed(title='Whitelist Application Responded', description=f'**Member** \n {member.mention}({member.id}) \n **Result** \n {res} \n **Approved by** \n {ctx.author.mention} ({ctx.author.id})')
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar.url}')
        embed.set_footer(text=server_name, icon_url=server_logo)
        embed.set_thumbnail(url=server_logo)
        await admin_log.send(f'{member.name} application {res} by {ctx.author.name}')
        await log_channel.send(embed=embed)
    except Exception as e:
        print(e)
#============================================= Announce ==============================
@bot.command('announce')
@commands.has_any_role(staff_id, admin_role_id)
async def announce(ctx, *message):
    msg = ' '.join(message)
    
    if msg is not None:
        announce_channel = bot.get_channel(announcement_id)
        if '~' in msg:
            lines = msg.split('~')
            for line in lines:
                await announce_channel.send(line)
        else:
            await announce_channel.send(msg)
            
    await ctx.message.delete()
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(title='Announcement Sent', description=msg)
    embed.timestamp = datetime.datetime.now()
    embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar.url}')
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    await log_channel.send(embed=embed)
    
#============================================= Say ==============================
@bot.command('say')
@commands.has_any_role(staff_id, admin_role_id)
async def say(ctx, *message):
    msg = ' '.join(message)
    
    if msg is not None:
        if '~' in msg:
            lines = msg.split('~')
            for line in lines:
                await ctx.send(line)
        else:
            await ctx.send(msg)
            
    await ctx.message.delete()
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(title='Say Command Used', description=msg)
    embed.timestamp = datetime.datetime.now()
    embed.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar.url}')
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    await log_channel.send(embed=embed)
 
@bot.command(name='user')
async def user(ctx):
    try:
        author = ctx.author
        log_channel = bot.get_channel(log_channel_id)
        user_info_channel = bot.get_channel(user_info)
        if ctx.message.channel.id != user_info:
            await log_channel.send(f'`{ctx.author.name} has tried to check thier info in {ctx.message.channel.name}` ❌')
            await ctx.reply(f'You cannot execute this command here. Please use {user_info_channel.mention} channel')
            return
        embed = discord.Embed(color=discord.Color.red(), title=f'{ctx.author.global_name}', description='')
        embed.timestamp = datetime.datetime.now()
        created_at = author.created_at.strftime('%Y/%m/%d, %H:%M:%S')
        embed.add_field(name='User', value=f'{author.mention}')
        embed.add_field(name='ID', value=f'`{author.id}`')
        embed.add_field(name='Created at', value=f'`{created_at}`')
        embed.add_field(name='Top Role', value=f'{author.top_role.mention}')
        embed.set_footer(text=f'{bot.user.name}', icon_url=server_logo)
        embed.set_author(name=f'{ctx.author.name}#{author.discriminator}', icon_url=f'{ctx.author.avatar.url}')
        embed.set_thumbnail(url=f'{author.avatar.url}')
        #await ctx.message.delete()
        await ctx.reply(embed=embed)
        await log_channel.send(f'`{ctx.author.name} has checked thier info in user channel` ✅')
    except Exception as e:
        print(e)
   
@tree.command(name='help', description='Show Command List', guild=discord.Object(server_id))
@app_commands.checks.has_any_role(staff_id, admin_role_id)
async def help(interaction:discord.Interaction):
    embed = discord.Embed(color=theme_color, description='Here is the all commands that use with this bot', title='Command List')
    embed.timestamp = datetime.datetime.now()
    embed.set_author(name=f'{bot.user.name}')
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.add_field(name='?rs <discordid> <pass/fail>', value='Send Application respond. (Only for Staff)', inline=False)
    embed.add_field(name='?announce <annoucement>', value='Send An Annoucement to Annoucement Channel. (Use ~ to break lines) (Only for Staff)', inline=False)
    embed.add_field(name='?say <message>', value='Send a Message through bot in any channel. (Use ~ to break lines) (Only for Staff)', inline=False)
    embed.add_field(name='?setupticket', value='Setup Tickets. (Only for Staff)', inline=False)
    embed.add_field(name='?user', value='Get User Info in any specific channel.  (Can be used by anyone)', inline=False)
    embed.add_field(name='/add', value='Add a member to ticket. (Only Staff)', inline=False)
    embed.add_field(name='/remove', value='Remove a member from ticket. (Only Staff)', inline=False)
    embed.add_field(name='/close', value='Close a ticket(Staff Only)', inline=False)
    embed.add_field(name='/reopen', value='Reopen a closed ticket', inline=False)
    embed.add_field(name='/help', value='Get Command List', inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)
#============================================= Tickets ==============================
@bot.command('setupticket')
@commands.has_any_role(staff_id, admin_role_id)
async def setupticket(ctx):
    try:
        embed = discord.Embed(title='Create a Ticket', description='Click below button to create a ticket. Our staff will respond shortly 📩', color=discord.Color.blue())
        embed.set_author(name=f'{bot.user.name}', icon_url=server_logo)
        embed.timestamp = datetime.datetime.now()
        view = discord.ui.View()
        view.add_item(SetupButton())
        view.add_item(SetupButton2())
        await ctx.send(embed=embed, view=view)
    except Exception as e:
        print(e)
        
@tree.command(name='close', description='Close an opened ticket', guild=discord.Object(id=server_id))
@app_commands.checks.has_any_role(staff_id, admin_role_id)
async def close(interaction: discord.Interaction):
    try: 
        channel = interaction.channel
        member = None
        name = channel.name
        if not 'ticket' in name:
            await interaction.response.send_message('This is not an ticket')
        else:
            old = channel.name
            closed_name = 'closed-' + channel.name
            category = discord.utils.get(interaction.guild.categories, name='Closed Tickets')
            if not category:
                category = await interaction.guild.create_category('Closed Tickets')
            with open('ticket.json') as file:
                data = json.load(file)
                channelid = str(channel.id)
                if channelid in data:
                    memberid = data[channelid]['id']
                    member = interaction.guild.get_member(memberid)
                    
            await channel.edit(name=closed_name)
            await channel.edit(category=category)
            await channel.set_permissions(member, view_channel = False, send_messages = False, attach_files = False, embed_links = False)
            embed = discord.Embed(description=f'Ticket has been closed by {interaction.user.name}')
            await interaction.response.send_message(embed=embed)
            
        log_channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(title='Closed Ticket', description=f'**Ticket** \n {channel.name}')
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar.url}')
        embed.set_footer(text=server_name, icon_url=server_logo)
        embed.set_thumbnail(url=server_logo)
        await log_channel.send(embed=embed)
    except Exception as e:
        print(e)

@tree.command(name='add', description='Add Person to Ticket', guild=discord.Object(server_id))
@app_commands.checks.has_any_role(staff_id, admin_role_id)
async def add(interaction: discord.Interaction, member: discord.Member):
    channel = interaction.channel
    
    if not channel.name.startswith('ticket'):
        await interaction.response.send_message('This is not a ticket')
    else:
        await channel.set_permissions(member, view_channel = True, send_messages = True, embed_links = True, attach_files = True)
    
    embed = discord.Embed(description=f'{member.mention} added to ticket')
    await interaction.response.send_message(embed=embed)
    
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(title='Added to Ticket', description=f'**Ticket** \n {channel.name} \n **Member** \n {member.name} ({member.id})')
    embed.timestamp = datetime.datetime.now()
    embed.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar.url}')
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    await log_channel.send(embed=embed)
    
@tree.command(name='remove', description='Remove Person from Ticket', guild=discord.Object(server_id))
@app_commands.checks.has_any_role(staff_id, admin_role_id)
async def add(interaction: discord.Interaction, member: discord.Member):
    channel = interaction.channel
    
    if not channel.name.startswith('ticket'):
        await interaction.response.send_message('This is not a ticket')
    else:
        await channel.set_permissions(member, view_channel = False, send_messages = False, embed_links = False, attach_files = False)
    
        embed = discord.Embed(description=f'{member.mention} removed from ticket')
        await interaction.response.send_message(embed=embed)
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(title='Removed from Ticket', description=f'**Ticket** \n {channel.name} \n **Member** \n {member.name} ({member.id})')
    embed.timestamp = datetime.datetime.now()
    embed.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar.url}')
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    await log_channel.send(embed=embed)
    
@tree.command(name='reopen', description='Reopen closed Ticket', guild=discord.Object(server_id))
@app_commands.checks.has_any_role(staff_id, admin_role_id)
async def reopen(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    channel = interaction.channel
    member = None
    if not channel.name.startswith('closed'):
        await interaction.followup.send('This is not a ticket')
    else:
        old = channel.name
        closedname = old.replace('closed-','')
        category = discord.utils.get(interaction.guild.categories, name='Reopened Tickets')
        if not category:
            category = await interaction.guild.create_category('Reopened Tickets')
        with open('ticket.json') as file:
            data = json.load(file)
                
            channelid = str(channel.id)
            if channelid in data:
                memberid = data[channelid]['id']
                member = interaction.guild.get_member(memberid)
            else:
                 await interaction.followup.send("Something error Occured")
                    
        await channel.edit(name=closedname)
        await channel.edit(category=category)
        await channel.set_permissions(member, view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        embed = discord.Embed(description=f'Ticket has been reopened by {interaction.user.name}')
        await interaction.followup.send(embed=embed)
            
        log_channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(title='Reopned Ticket', description=f'**Ticket** \n {channel.name}')
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=f'{interaction.user.name}', icon_url=f'{interaction.user.avatar.url}')
        embed.set_footer(text=server_name, icon_url=server_logo)
        embed.set_thumbnail(url=server_logo)
        await log_channel.send(embed=embed)
        

#------------------------------------------------- Events ---------------------------------------------
@bot.event
async def on_member_update(before, after):
    guild = before.guild
    if guild.id != server_id:
        return
    
    whitelist_log = bot.get_channel(whitelist_log_id)
    banned_log = bot.get_channel(banned_log_id)
    time = datetime.datetime.now()
    zone = pytz.timezone('Asia/Colombo')
    date = time.astimezone(zone).strftime('%Y/%m/%d, %H:%M:%S')
    
    if len(after.roles) > len(before.roles):
        added_roles = set(after.roles) - set(before.roles)
        role = None
        
        for r in added_roles:
            role = r
            
        async for act in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
            target = act.target
            mod = act.user
            
            if role.id == whitelist_id:
                with open('whitelist.json') as db:
                    data = json.load(db)
                    
                    targetid = str(target.id)
                    modid = str(mod.id)
                    if targetid in data:
                        data[targetid] = {
                            'member':data[targetid]['member'],
                            'memberid':data[targetid]['memberid'],
                            'moderator':mod.name,
                            'moderatorid':modid,
                            'time':date
                        }
                    else:
                        data[targetid] = {
                            'member':target.name,
                            'memberid':targetid,
                            'moderator':mod.name,
                            'moderatorid':modid,
                            'time':date
                        }
                    with open('whitelist.json', 'w') as f:
                        json.dump(data,f,indent=5)
                await whitelist_log.send(f'`{target.name} ({target.id}) has been whitelisted by {mod.name} ({mod.id}) | Time - {date} ✅`') 
                log_channel = bot.get_channel(log_channel_id)
                embed = discord.Embed(title='Member Whitelisted', description=f'**Member** \n {target.name} ({target.id})', color=green)
                embed.timestamp = datetime.datetime.now()
                embed.set_author(name=f'{mod.name}', icon_url=f'{mod.avatar.url}')
                embed.set_footer(text=server_name, icon_url=server_logo)
                embed.set_thumbnail(url=server_logo)
                await log_channel.send(embed=embed)
        
    if len(after.roles) < len(before.roles):
        removed_roles = set(before.roles) - set(after.roles)
        role = None
        
        for r in removed_roles:
            role = r
            
        async for act in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
            target = act.target
            mod = act.user
            
            if role.id == whitelist_id:
                with open('ban.json') as db:
                    data = json.load(db)
                    time = datetime.datetime.now()
                    zone = pytz.timezone('Asia/Colombo')
                    date = time.astimezone(zone).strftime('%Y/%m/%d, %H:%M:%S')
                    targetid = str(target.id)
                    modid = str(mod.id)
                    if targetid in data:
                        data[targetid] = {
                            'member':data[targetid]['member'],
                            'memberid':data[targetid]['memberid'],
                            'moderator':mod.name,
                            'moderatorid':modid,
                            'time':date
                        }
                    else:
                        data[targetid] = {
                            'member':target.name,
                            'memberid':targetid,
                            'moderator':mod.name,
                            'moderatorid':modid,
                            'time':date
                        }
                    with open('ban.json', 'w') as f:
                        json.dump(data,f,indent=5)
                        
                await banned_log.send(f'`{target.name} ({target.id}) whitelist has been removed by {mod.name} ({mod.id}) | Time - {date} ❌`')
                log_channel = bot.get_channel(log_channel_id)
                embed = discord.Embed(title='Member Whitelist Removed', description=f'**Member** \n {target.name} ({target.id})', color=red)
                embed.timestamp = datetime.datetime.now()
                embed.set_author(name=f'{mod.name}', icon_url=f'{mod.avatar.url}')
                embed.set_footer(text=server_name, icon_url=server_logo)
                embed.set_thumbnail(url=server_logo)
                await log_channel.send(embed=embed)
                
#----------------------------------------- Error Handling System ------------------------------
#================================================= Commands =========================
@bot.event
async def on_command_error(ctx, error):
    log_channel = bot.get_channel(log_channel_id)
    author = ctx.author
    command = ctx.message.content
    if isinstance(error, commands.errors.MissingAnyRole):
        await ctx.reply('You are missing required roles')
        await log_channel.send(f'`{author} has tried to excute {command} in {ctx.message.channel.name} ❌`')
    elif isinstance(error, commands.errors.MissingRole):
        await ctx.reply('You are missing required role')
        await log_channel.send(f'`{author} has tried to excute {command} in {ctx.message.channel.name} ❌`')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply('You are missing an required arguement. Please check commands')
        await log_channel.send(f'`{author} has tried to excute {command} in {ctx.message.channel.name} ❌`')
    elif isinstance(error, commands.errors.BotMissingPermissions):
        await ctx.reply('I dont have permissions to execute this commands')
        await log_channel.send(f'`{author} has tried to excute {command} in {ctx.message.channel.name} ❌`')
    elif isinstance(error, commands.errors.ArgumentParsingError):
        await ctx.reply('An error occured while parsing the arguments. Please contact developer')
        await log_channel.send(f'`{author} has tried to excute {command} in {ctx.message.channel.name} ❌`')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.reply('Command Not Found')
        await log_channel.send(f'`{author} has tried to excute {command} in {ctx.message.channel.name} ❌`')
    elif isinstance(error, commands.errors.CommandError):
        await ctx.reply('Command Error. Please contact the developer')
        await log_channel.send(f'`{author} has tried to excute {command} in {ctx.message.channel.name} ❌`')
        
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    log_channel = bot.get_channel(log_channel_id)
    author = interaction.user
    command = interaction.command.name
    if isinstance(error, app_commands.errors.MissingRole):
        embed = discord.Embed(color=discord.Color.red(), description="You don't have Required Role")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await log_channel.send(f'`{author} has tried to excute {command} in {interaction.channel.name} ❌`')
    elif isinstance(error, app_commands.errors.BotMissingPermissions):
        embed = discord.Embed(color=discord.Color.red(), description="Bot doesn't have required permission to execute command")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await log_channel.send(f'`{author} has tried to excute {command} in {interaction.channel.name} ❌`')
    elif isinstance(error, app_commands.errors.BotMissingPermissions):
        embed = discord.Embed(color=discord.Color.red(), description="You don't have any required roles")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await log_channel.send(f'`{author} has tried to excute {command} in {interaction.channel.name} ❌`')
    


asyncio.run(main())
    

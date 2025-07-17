import discord
import datetime
from discord.ext import commands
from easy_pil import *

# ====== Your Server Specific IDs ======
server_id = 1376872792242389012
welcome_channel_id = 1376872792879796319
log_channel_id = 1376872792879796323
member_role_id = 1376872792242389018
# ======================================

class Welcome(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Welcome Cog Loaded')
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != server_id:
            return
        
        welcome_channel = self.bot.get_channel(welcome_channel_id)
        log_channel = self.bot.get_channel(log_channel_id)
        member_role = member.guild.get_role(member_role_id)
        
        background = Editor('welcome.png')
        profile_image = await load_image_async(str(member.avatar.url))
        
        profile = Editor(profile_image).resize((400, 400)).circle_image()
        poppins = Font.poppins(size=100, variant='bold')
        poppins_small = Font.poppins(size=35, variant="light")
        
        background.paste(profile, (440, 185))
        background.text((620, 60), 'Welcome', color='#ffffff', font=poppins, align='center')
        background.text((648, 623), f'{member.name}#{member.discriminator}', color='#ffffff', font=poppins_small, align='center')
        
        file = discord.File(fp=background.image_bytes, filename='welcome.png')
        msg = f'{member.mention} Welcome to Our Server Gta V Roleplay Srilanka'
        
        await welcome_channel.send(file=file)
        await welcome_channel.send(msg)
        await member.add_roles(member_role)
        
        # ---------------- Log Embed --------------------
        date = member.created_at.strftime('%d/%m/%Y : %H:%M:%S')
        embed = discord.Embed(color=discord.Color.green(), title='Member Joined')
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar.url}')
        embed.add_field(name='ID', value=f'`{member.id}`')
        embed.add_field(name='User', value=f'{member.mention}')
        embed.add_field(name='Created', value=f'`{date}`')
        embed.set_footer(text=f'{self.bot.user}')
        embed.set_thumbnail(url=f'{member.avatar.url}')
        
        await log_channel.send(embed=embed)

    @commands.command(name='welcometest')
    async def welcometest(self, ctx, memberid):
        try:
            member = ctx.guild.get_member(int(memberid))
            if not member:
                await ctx.send("Invalid member ID or member not in this server.")
                return

            welcome_channel = self.bot.get_channel(welcome_channel_id)
            log_channel = self.bot.get_channel(log_channel_id)
            member_role = member.guild.get_role(member_role_id)
            
            background = Editor('banner.png')
            profile_image = await load_image_async(str(member.avatar.url))
            
            profile = Editor(profile_image).resize((400, 400)).circle_image()
            poppins = Font.poppins(size=100, variant='bold')
            poppins_small = Font.poppins(size=35, variant="light")
            
            background.paste(profile, (440, 185))
            background.text((620, 60), 'Welcome', color='#ffffff', font=poppins, align='center')
            background.text((648, 623), f'{member.name}#{member.discriminator}', color='#ffffff', font=poppins_small, align='center')
            
            file = discord.File(fp=background.image_bytes, filename='welcome.png')
            msg = f'{member.mention} Welcome to SouthSide RolePlay'
            
            await welcome_channel.send(file=file)
            await welcome_channel.send(msg)
            await member.add_roles(member_role)

            date = member.created_at.strftime('%d/%m/%Y : %H:%M:%S')
            embed = discord.Embed(color=discord.Color.green(), title='Member Joined')
            embed.timestamp = datetime.datetime.now()
            embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar.url}')
            embed.add_field(name='ID', value=f'`{member.id}`')
            embed.add_field(name='User', value=f'{member.mention}')
            embed.add_field(name='Created', value=f'`{date}`')
            embed.set_footer(text=f'{self.bot.user}')
            embed.set_thumbnail(url=f'{member.avatar.url}')
            
            await log_channel.send(embed=embed)
        
        except Exception as e:
            print(f"Error in welcometest command: {e}")
            await ctx.send("Something went wrong during the test.")

# Bot cog setup
async def setup(bot):  
    await bot.add_cog(Welcome(bot))

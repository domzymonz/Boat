import discord
import discord.ext
import random
import typing
import re
import psutil
import socket
from platform import python_version
from datetime import datetime, timedelta
from discord import __version__ as discord_version
from PIL import ImageColor, Image
from discord.ext import commands
from psutil import Process, virtual_memory
from time import time

class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=["si"])
  async def serverinfo(self, ctx):

    statuses = [len(list(filter(lambda m: str(m.status) == "online" and not m.bot, ctx.guild.members))),
		len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
		len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
		len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
    info_emb=discord.Embed(
      title= 'Information',
      timestamp=datetime.utcnow(),
    )
    info_emb.set_thumbnail(url=ctx.guild.icon_url)
    info_emb.set_footer(text=f'Server Created At | {ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S")}', icon_url=ctx.guild.icon_url)
    fields=[
      ('__Server Information__',
        f'**Server Name** : {ctx.message.guild.name}\n'\
        f'**ID** : {ctx.guild.id}\n'\
        f'**Owner** : <@{ctx.guild.owner.id}>\n'\
        f'**Region** : {str(ctx.guild.region).capitalize()}\n'\
        f'**Created at** : {ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S")}',False),
      ('__Server Boosts__',
        f'**Server Boost Level** : {ctx.guild.premium_tier}\n'\
        f'**Server Boosts** : {ctx.guild.premium_subscription_count}', False),
      ('__Member Information__',
        f'**Members** : {len(ctx.guild.members)} = \n'\
        f' **- Users** : {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}\n'\
        f' **- Bots** : {len(list(filter(lambda m: m.bot, ctx.guild.members)))}\n'\
        f'**Status** =\n'\
        f' **- :green_circle: Online : ** {statuses[0]}\n'\
        f' **- :crescent_moon: Idle : ** {statuses[1]}\n'\
        f' **- :o: Do Not Disturb : ** {statuses[2]}\n'\
        f' **- :radio_button: Offline : ** {statuses[3]}\n'\
        f'**Banned Members** : {len(await ctx.guild.bans())}', False),
      ('__Channel Information__',
        f'**Channel Categories** : {len(ctx.guild.categories)}\n'\
        f'**Channels** : {len(ctx.guild.channels)} =\n'\
        f' **- Text Channels** : {len(ctx.guild.text_channels)}\n **- Voice Channels** : {len(ctx.guild.voice_channels)}\n'\
        f'**Roles** : {len(ctx.guild.roles)}\n'\
        f'**Invites** : {len(await ctx.guild.invites())}', False),
      ('__Emoji Information__',
        f'**Emoji Limit** : {50 if ctx.guild.premium_tier == 0 else(100 if ctx.guild.premium_tier == 1 else(150 if ctx.guild.premium_tier == 2 else 250))}\n'\
        f'**Emojis** : {len(ctx.guild.emojis)} =\n'\
        f'**- Animated** : {len(list(filter(lambda e: e.animated,ctx.guild.emojis)))}\n'\
        f' **- Static** : {len(list(filter(lambda e: e.animated == False,ctx.guild.emojis)))}', False)
    ]
    for name, value, inline in fields:
      info_emb.add_field(
        name=name,
        value=value,
        inline=inline
      )
    await ctx.send(embed=info_emb)

  @commands.command(aliases=["memberinfo", "ui", "mi"])
  async def userinfo(self, ctx, target:discord.Member=None):
    target = target if target != None else ctx.author
    status = '<:online:811097047611473951> Online' if  target.is_on_mobile()==False and str(target.status)=="online" else ('<:online_phone:811096399512338453> Online (mobile)' if  target.is_on_mobile()==True and str(target.status)=="online" else ('<:idle:811097101253214209> Idle'if target.is_on_mobile() == False and str(target.status)=="idle" else ('<:idle_phone:811096480982368316> Idle (mobile)' if target.is_on_mobile() == True and str(target.status)=="idle" else ('<:dnd:811097075756040244> Do Not Disturb'if target.is_on_mobile() == False and str(target.status)=="dnd" else ('<:dnd_phone:811096437093957692> Do not Disturb (mobile)' if target.is_on_mobile() == True and str(target.status)=="dnd" else '<:offline:811097120319995905> Offline')))))
    activity = f"{str(target.activity.type).split('.')[-1].title() if target.activity else ''} {'=' if target.activity != None else ''} {str(target.activity)}"
    flag = list(target.public_flags)
    house = "<:hypesquad_bravery:811084230141411338> Bravery" if flag[4][1] else ("<:hypesquad_balance:811084218288439316> Balance" if flag[6][1] else ("<:hypesquad_briliance:811084170024583229> Brilliance" if flag[5][1] else "<:hypesquad_nohouse:811086260335935529> Houseless"))
    info_emb=discord.Embed(
      title= 'User Information',
      timestamp=datetime.utcnow(),
      colour=target.colour
    )
    info_emb.set_thumbnail(url=target.avatar_url)
    info_emb.set_footer(text=f'Member Joined At | {target.joined_at.strftime("%d/%m/%Y %H:%M:%S")}', icon_url=ctx.guild.icon_url)
    roles_str=""
    for role in target.roles:
      roles_str+=f"{role.mention}\n"
    fields=[
      ('__General Information__',
        f'**Name** : {str(target)}\n'\
        f'**Display Name** : {target.display_name}\n'\
        f'**ID** : `{target.id}`\n'\
        f'**Hypesquad House** : {house}\n'\
        f'**Created At** : `{target.created_at.strftime("%d/%m/%Y %H:%M:%S")}`\n'\
        f'**Bot?** {str(target.bot)+" == **Verified?** "+str(flag[12][1]) if target.bot==True else target.bot}',
      False),
      ('__Status and Activity__',
        f'**Status** : {status}\n'\
        f'**Activity** : {activity}',
      False),
      ('__Server Information__',
        f'**Top Role** : {target.top_role.mention}\n'\
        f'**Joined At** : `{target.joined_at.strftime("%d/%m/%Y %H:%M:%S")}`\n'\
        f'**Server Booster?** : {bool(target.premium_since)}\n',
      False),
      ('__Flags__',
        f'**Discord Partner** : {flag[1][1]}\n'\
        f'**Staff** : {flag[0][1]}\n'\
        f'**System User** : {flag[9][1]}\n'\
        f'**Early Supporter** : {flag[7][1]}\n'\
        f'**Team User** : {flag[8][1]}\n',
      False),
      ('__Roles__',
        f'{roles_str}',
      False)
    ]
    for name, value, inline in fields:
      info_emb.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=info_emb)

  @commands.command(aliases = ['stats', 'bs', 'botstats'])
  async def botstatistics(self, ctx):
    embed = discord.Embed(
      title = 'Bot Statistics',
      colour=ctx.guild.get_member(self.bot.user.id).color,
    )
    proc = Process()
    with proc.oneshot():
      delta_uptime = time()-proc.create_time()
      hours, remainder = divmod(int(delta_uptime), 3600)
      minutes, seconds = divmod(remainder, 60)
      days, hours = divmod(hours, 24)
      uptime=f"{days}d, {hours}h, {minutes}m, {seconds}s"
      cpu_use = psutil.cpu_percent()
      cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
      mem_total = virtual_memory().total / (1024**2)
      mem_of_total = proc.memory_percent()
      mem_usage = mem_total * (mem_of_total / 100)
    server = ''
    for servers in self.bot.guilds:
      server += f'- {servers.name}\n'
    fields = [
      ("__Programming Info__",
        f'**Python Version** : {python_version()}\n'\
        f'**discord.py Version** : {discord_version}\n'\
        f'**Hostname** : {socket.gethostname()}',
        False
      ),
      ('__Performance__',
        f'**Uptime** : {uptime}\n'\
        f'**CPU Time** : {cpu_time}\n'\
        f'**CPU Usage** : {cpu_use}%\n'\
        f'**Memory Usage** : {mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)',
        False
      ),
      ('__Socials__',
        f'**Users** : {len(self.bot.users)}\n'\
        f'**Servers** : {len(self.bot.guilds)} = \n'\
        f'{server}', False
      ),
      ('__API__',
        f'**Latency** : `{round(self.bot.latency,4)*1000}ms/{self.bot.ws._max_heartbeat_timeout}ms`\n'\
        f'**API Ratelimit** : `{self.bot.ws._rate_limiter.remaining}/{self.bot.ws._rate_limiter.max}`',
        False
      ),
      ('__Interactions__',
        f'**Cached Messages** : `{len(self.bot.cached_messages)}`\n'\
        f'**DMs opened** : `{len(self.bot.private_channels)}`',
        False
      )
    ]
    for name, value, inline in fields:
      embed.add_field(
        name = name,
        value = value,
        inline = inline
      )
    await ctx.send(embed = embed)

  @commands.command()
  async def id(self, ctx, emoji:discord.Emoji):
    await ctx.send(emoji.id)

  @commands.command()
  async def roleinfo(self, ctx, role:discord.Role):
    created_at=role.created_at.strftime("%d/%m/%Y %H:%M:%S")
    embed = discord.Embed(
      title="Role information",
		  colour=role.color,
		  timestamp=datetime.utcnow()
    )
    fields = [
      (
        "__General Info__", 
        f"Mention: {role.mention}\n"\
        f"Name: {role.name}\n"\
        f"ID: {role.id}\n"\
        f"Guild: {role.guild.name}\n"\
      , False),
      (
        "__Other Info__", 
        f"Created at: {created_at}\n"\
        f"Position: #{len(ctx.guild.roles)-(role.position)}\n"\
        f"Color: {role.color}\n"\
        f"Members: {len(role.members)}\n"\
      , False),
      (
        "__Role Settings__", 
        f"Everyone role: {role.is_default()}\n"\
        f"Admin: {role.permissions.administrator}\n"\
        f"Hoisted: {role.hoist}\n"\
        f"Managed by Integration: {role.managed}\n"\
      , False)
    ]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Info(bot))
  print ('Loaded Information Cog Successfully!')
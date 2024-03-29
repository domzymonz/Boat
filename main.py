import discord
import os
import difflib
import sys
import letitlive
import custom
import subprocess
from replit import db
from discord.ext import commands
from datetime import datetime
from datetime import timedelta

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'discord_components'])
import discord_components as dc

bot = commands.Bot(
  command_prefix=['b?', 'B?'],
  intents=discord.Intents.all(),
  owners=[737422322431950962,557599092931559447, 798743649809727519,726314322565005382]
)
ddb = dc.DiscordComponents(bot)

@bot.event
async def on_ready():
  print("Ready!")
  for item in db:
    custom.files.json_load_backup(str(item))
fail_emb = discord.Embed(title = 'Error: Missing extension', color = 0xFFFFFF)

@bot.command(aliases = ['l'])
@commands.is_owner()
async def load(ctx, extension = None):
  if extension == None:
    await ctx.message.delete()
    await ctx.send(embed=fail_emb, delete_after=3.0)
    return 0
  bot.load_extension(f'cogs.{extension}')
  embed=discord.Embed(title = f'Loading: cogs.{extension}', color = 0x228B22)
  await ctx.message.delete()
  await ctx.send(embed=embed, delete_after=3.0)

@bot.command(aliases = ['u'])
@commands.is_owner()
async def unload(ctx, extension):
  if extension == None:
    await ctx.message.delete()
    await ctx.send(embed=fail_emb, delete_after=3.0)
    return 0
  bot.unload_extension(f'cogs.{extension}')
  embed=discord.Embed(title = f'Unloading: cogs.{extension}', color = 0x800000)
  await ctx.message.delete()
  await ctx.send(embed = embed, delete_after=3.0)

@bot.command(aliases = ['r'])
@commands.is_owner()
async def reload(ctx, extension='all'):
  if extension == None:
    await ctx.message.delete()
    await ctx.send(embed=fail_emb, delete_after=3.0)
    return 0
  if extension == 'all':
    await ctx.message.delete()
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        try:
          bot.unload_extension(f'cogs.{filename[:-3]}')
        finally:
          bot.load_extension(f'cogs.{filename[:-3]}')
          embed=discord.Embed(title = f'Reloading: cogs.{filename}', color = 0x241571)
          await ctx.send(embed=embed, delete_after=3.0)
    return 0
  try:
    bot.unload_extension(f'cogs.{extension}')
  except:
    pass
  finally:
    bot.load_extension(f'cogs.{extension}')
    embed=discord.Embed(title = f'Reloading: cogs.{extension}', color = 0x241571)
    await ctx.message.delete()
    await ctx.send(embed=embed, delete_after=3.0)

@bot.command()
@commands.is_owner()
async def list(ctx):
  loaded = []
  emb_desc = []
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      try:
        bot.load_extension(f'cogs.{filename[:-3]}')
        bot.unload_extension(f'cogs.{filename[:-3]}')
      except discord.ext.commands.ExtensionAlreadyLoaded:
        loaded.append(filename[:-3])
  for cog in loaded:
    emb_desc.append(f'- {cog}')
  load_emb = discord.Embed(title = 'Loaded Cogs', description = ('\n'.join(emb_desc)), color = 0xFFA500)
  await ctx.message.delete()
  await ctx.send(embed=load_emb, delete_after=3.0)

@bot.command(aliases=['rb', 'restartbot'])
@commands.is_owner()
async def restart(ctx):
  await ctx.message.delete()
  os.execl(sys.executable, sys.executable, *sys.argv)
  
@bot.command()
async def dropdown(ctx):
  await ctx.send(content='test',
    components=[dc.Select(options=[dc.Option(label='Option 1', value='1'), dc.Option(label='Option 2', value = '2')])]
  )

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

letitlive.keep_alive()
bot.run(os.environ.get("TOKEN"))
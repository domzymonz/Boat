import math
import discord
import os
import re
import requests
import asyncio
import json
import aiocron
import random
import datetime
from PIL import Image
from PIL import ImageColor
from discord.ext import commands, tasks
from mcstatus import MinecraftServer


'''    activeservers = list(self.bot.guilds)
    servers=[]
    for activeserver in activeservers:
      servers.append(activeserver.name)'''

class Test(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def test(self, ctx):
    number = 1
    gap = 1
    message = await ctx.send(number)
    while True:
      reactions = ['⏪', '⏺' ,'⏩']
      for reaction in reactions:
        await message.add_reaction(reaction)
      def check (reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
      reaction = await self.bot.wait_for('reaction_add', check=check)
      if str(reaction[0]) == '⏪':
        try:
          number = number - gap
          await message.remove_reaction(str(reaction[0]), ctx.author)
          await message.edit (content=number)
        except:
          await message.delete()
          message = await ctx.send(number)
      elif str(reaction[0]) == '⏩':
        try:
          number = number + gap
          await message.remove_reaction(str(reaction[0]), ctx.author)
        except:
          await message.delete()
          message = await ctx.send(number)
        await message.edit (content=number)
      else:
        try:
          await message.remove_reaction(str(reaction[0]), ctx.author)
          await message.delete()
          await ctx.send (number)
          break
        except:
          await message.delete()
          message = await ctx.send(number)
          break

  @commands.command()
  async def test1(self, ctx):
    number = 0
    gap = 1
    message = await ctx.send(number)
    reactions = ['⏺️', '0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣', '◀️', '⏪', '🔙']
    for reaction in reactions:
      await message.add_reaction(reaction)
    while True:
      def check (reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
      reaction = await self.bot.wait_for('reaction_add', check=check)
      if str(reaction[0]) == '0️⃣':
        number = (number * 10) + 0
      elif str(reaction[0]) == '1️⃣':
        number = (number * 10) + 1
      elif str(reaction[0]) == '2️⃣':
        number = (number * 10) + 2
      elif str(reaction[0]) == '3️⃣':
        number = (number * 10) + 3
      elif str(reaction[0]) == '4️⃣':
        number = (number * 10) + 4
      elif str(reaction[0]) == '5️⃣':
        number = (number * 10) + 5
      elif str(reaction[0]) == '6️⃣':
        number = (number * 10) + 6
      elif str(reaction[0]) == '7️⃣':
        number = (number * 10) + 7
      elif str(reaction[0]) == '8️⃣':
        number = (number * 10) + 8
      elif str(reaction[0]) == '9️⃣':
        number = (number * 10) + 9
      elif str(reaction[0]) == '◀️':
        number = (number / 10)
      elif str(reaction[0]) == '⏺️':
        await message.clear_reactions()
      elif str(reaction[0]) == '⏪':
        number = 0
      elif str(reaction[0]) == '🔙':
        await message.delete()
      number = int(number)
      await message.remove_reaction(str(reaction[0]), ctx.author)
      await message.edit(content = number)

  @commands.command()
  async def test2(self, ctx):
    server = requests.get('https://api.bedrockinfo.com/v1/status?server=blocksense.ddns.net&port=25608')
    js = server.json()
    embed = discord.Embed(title = re.sub(r"§[0-9A-GK-OR]","",js["ServerName"],count=0,flags=(re.I)))
    embed.add_field(name="Online Players",value=js["Players"])
    embed.add_field(name="Max Players",value=js["MaxPlayers"])
    embed.add_field(name="Map Name",value=re.sub(r"§[0-9A-GK-OR]","",js["MapName"],count=0,flags=(re.I)))
    embed.add_field(name="Default Gamemode",value=js["GameMode"],inline=False)
    embed.add_field(name="Minecraft Version",value=js["Version"])
    embed.add_field(name="Minecraft Server Timestamp",value=js["CheckTimestamp"])
    await ctx.send(embed=embed)#cool
  
  @commands.command()
  async def test3(self, ctx):
    c_channels = [ctx.channel]
    channels = []
    for channel in ctx.guild.text_channels:
      permission = ctx.author.permissions_in(channel).send_messages
      if permission == True:
        channels.append(channel)
    index = 0
    embed = discord.Embed(
      title = 'Select Channel',
      description = 'Please select the channel you want to relocate the call. You can do so by reacting with the corresponding emote.',
      color = 0xef7d57
    )
    embed.add_field(
      name = f'{index + 1}: {channels[index].name}',
      value = f'ID: {channels[index].id}',
      inline = False
    )
    message = await ctx.send(embed=embed)
    while True:
      if index == 0:
        reactions = ['⏺' ,'⏩']
        add = ['🟦', '⏺' ,'⏩']
      elif index + 1 == len(channels):
        reactions = ['⏪', '⏺']
        add = ['⏪', '⏺', '🟦']
      else:
        reactions = ['⏪', '⏺' ,'⏩']
        add = reactions
      for reaction in add:
        await message.add_reaction(reaction)
      def check (reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
      reaction = await self.bot.wait_for('reaction_add', check=check)
      if str(reaction[0]) == '⏪':
        index = index - 1
        embed = discord.Embed(
          title = 'Select Channel',
          description = 'Please select the channel you want to relocate the call. You can do so by reacting with the corresponding emote.',
          color = 0xef7d57
        )
        embed.add_field(
          name = f'{index + 1}: {channels[index].name}',
          value = f'ID: {channels[index].id}',
          inline = False
        )
        try:
          await message.clear_reactions()
          await message.edit (embed = embed)
        except:
          await message.delete()
          message = await ctx.send(embed = embed)
      elif str(reaction[0]) == '⏩':
        index = index + 1
        embed = discord.Embed(
          title = 'Select Server',
          description = 'Please select the server you want to relocate the call. You can do so by reacting with the corresponding emote.',
          color = 0xef7d57
        )
        embed.add_field(
          name = f'{index + 1}: {channels[index].name}',
          value = f'ID: {channels[index].id}',
          inline = False
        )
        try:
          await message.clear_reactions()
          await message.edit (embed = embed)
        except:
          await message.delete()
          message = await ctx.send(embed = embed)
      elif str(reaction[0]) == '⏺':
        await message.delete()
        id = channels[index].id
        channel = self.bot.get_channel(id)
        c_channels.append(channel)
        for c in c_channels:
          await ctx.send(f'<#{c.id}>')
        break
        
  @commands.command()
  async def test4 (self, ctx):
    embed=discord.Embed(color=0xffcd75)
    embed.set_author(name="Domzymonz#1900", icon_url="https://media.discordapp.net/attachments/800292729996967966/804197689092079616/Untitled16_20210124200535.png?width=473&height=473")
    fields = [
      ('------------------ General ------------------', '---------------------------------------------', False),
      ('🔇 Mute', 'Toggles mute in your party.', False),
      ('📻 Relocate', 'Relocates the party\'s location.', False),
      ('--------------- Call Settings ---------------', '---------------------------------------------', False),
      ('✉️ End', 'Ends the call if the other party accepts.', False),
      ('🔒 Force End', 'Forcefully ends the call.', False),
      ('-------------- Miscellaneous --------------', '---------------------------------------------', False),
      ('◀️ Back', 'Returns you to the call.', True)
    ]
    for name, value, inline in fields:
      embed.add_field(
        name = name,
        value = value,
        inline = inline or False
      )
    await ctx.send(embed=embed)
    
  @commands.command()
  async def test5 (self, ctx, user:discord.Member, *message):
    message = ' '.join(message)
    message = message.replace('b? ', 'b?')
    dm = await user.create_dm()
    await dm.send(message)
  
  @commands.command()
  async def test6(self, ctx):
    x, y = 10, 10
    maze = []
    for line in range(y):
      maze_line = []
      for _ in range(x):
        try:
          if maze_line[_-1] == '🟫':
            maze_line.append(random.choices(['🟨','🟩'], weights = [1, 2])[0])
          elif maze_line[_-1] == '🟨':
            maze_line.append(random.choices(['🟫','🟨','🟩'], weights = [1, 2, 1])[0])
          elif maze_line[_-1] == '🟩':
            maze_line.append(random.choices(['🟫','🟨'], weights = [2, 1])[0])
        except:
          maze_line.append(random.choices(['🟫','🟨','🟩'])[0])
      maze.append(maze_line)

    text = ''
    for _ in maze:
      text += (''.join(_)) + '\n'
    message = await ctx.send (text)

  @commands.Cog.listener()
  async def on_message(self, message):
    mention = '<@!416147488643481610>'
    if mention in message.content:
      await message.channel.send("You mentioned him")
      with open('json/cooldown.json') as f:
        cooldown = json.load(f)
      cooldown["last"] = str(datetime.datetime.now())
      with open('json/cooldown.json', 'w') as f:
        json.dump(cooldown, f)
  
  @tasks.loop(seconds=60)
  async def colour_change():
    with open('json/cooldown.json') as (f):
      cooldown = json.load(f)
    print ((datetime.datetime.now() - datetime.datetime.strptime(cooldown["last"], '%Y-%m-%d %H:%M:%S.%f')))
    
def setup(client):
  client.add_cog(Test(client))
  print ('Loaded Test Cog Successfully!')
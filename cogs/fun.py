import discord
from discord.ext import commands
import requests
import os
import random
from os import listdir
from os.path import isfile, join
import random
from PIL import ImageDraw, ImageFont, Image, ImageColor
from ImageColor import getrgb

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ['8ball'])
  async def eightball (self, ctx, *, question=None):
    if question == None:
      await ctx.send("Do you think that I am gonna answer to nothing?")
      return
    if question.endswith('?'):
      answers = [
        [
          f'Yes {ctx.author.mention}!',
          f'Yes {ctx.author.mention}, definitely!',
          f'I\'m sure! Yes {ctx.author.mention}!',
          f'Indeed {ctx.author.mention}...',
          f'Ummmmm. Yes {ctx.author.mention}.',
          f'Of course {ctx.author.mention}!',
          f'Yeah, {ctx.author.mention}.',
          f'It\'s clear that it\'s a yes, {ctx.author.mention}!',
          f'What? Are you kidding me? Yes!{ctx.author.mention}',
          f'{ctx.author.mention}, Yes...',
          f'Yup! {ctx.author.mention}'
        ],
        [
          f'Maybe? I\'m not quite sure {ctx.author.mention}',
          f'Maybe... {ctx.author.mention}',
          f'I\'m confused. But, maybe. {ctx.author.mention}',
          f'I don\'t know. {ctx.author.mention}',
          f'Ummmmmm. Idk {ctx.author.mention}',
          f'That is confusing, {ctx.author.mention}!',
          f'I don\'t really know, {ctx.author.mention}',
          f'Idk {ctx.author.mention}.',
          f'I do not know. {ctx.author.mention}'
          f'I\'m just a bot and I\'m not smart. {ctx.author.mention}'
        ],
        [
          f'No {ctx.author.mention}.',
          f'Nah {ctx.author.mention}.',
          f'Nope {ctx.author.mention}.',
          f'Ummmmmmmm. No. No. Nonono {ctx.author.mention}',
          f'No, I don\'t think so {ctx.author.mention}',
          f'Of course not {ctx.author.mention}.',
          f'Nay, Totally not {ctx.author.mention}.',
          f'Nope. {ctx.author.mention}',
          f'Totally not {ctx.author.mention}.',
          f'It\'s a no, {ctx.author.mention}'
        ]
      ]
      random.seed(f'{str(ctx.author.id)}{question.lower()}')
      answer_list = answers[random.randint(0, 2)]
      random.seed()
      await ctx.send (random.choices(answer_list)[0])
    else:
      await ctx.send(f"Do you really think it is a question  {ctx.author.mention}? *(Question must end with __?__)*")

  @commands.command(aliases = ['iw'])
  async def imagewrite(self, ctx, text, hexcolor = '#ffffff'):
    wide = 599
    hexcolor = getrgb(hexcolor)
    for x in range((len(text) // 18)):
      text = text[:(18 * x)] + '\n' + text[(18 * x):]
    barframe = Image.new('RGB', (620,60), color = (9, 80, 78))
    notbar = Image.new('RGB', (600,40), color = (90 , 90, 225))
    bar = Image.new('RGB', (wide,40), color = (30, 30, 225))
    out = Image.new("RGB", (2568, 1440), hexcolor)
    fnt = ImageFont.truetype("font/Minecraftia-Regular.ttf", 40)
    d = ImageDraw.Draw(out)
    d.multiline_text((10,40), text, font=fnt, fill=(0, 0, 0))
    out.paste(barframe,(424,335))
    out.paste(notbar,(434,345))
    out.paste(bar,(434,345))
    out.save('photos/text.jpg')
    with open('photos/text.jpg', 'rb') as e:
      await ctx.send(file = discord.File(e, 'photos/text.jpg'))

def setup(bot):
  bot.add_cog(Fun(bot))
  print ('Loaded Fun Cog Successfully!')
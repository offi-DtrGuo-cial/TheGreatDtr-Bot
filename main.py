# Webserver framework import
from legacy.redlight import keep_alive
keep_alive()

# Discord modules import
import discord
from discord.ext import commands

# File management imports
import os

# Other module imports
import asyncio

# Import supplementary scripts
from access_libr import B
from main_fam.early_rave import Early
from main_fam.hhc import Happy
from poke_world.pokemon import Pokedex as Poke
from hp_folder.hardpoints import Hard_Points as HP

# Extract private environmental variables
# print(os.environ)
TOKEN = os.environ.get('DISCORD_TOKEN')
GUILD = os.environ.get('DISCORD_GUILD')

GENERAL_ID = int(os.environ.get('GENERAL_ID'))

### BOT CONFIGURATION
# Set up bot instance
bot = commands.Bot(command_prefix='!')

# Initialisation message
@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')

# Early commands
@bot.command(name='hi')
async def hi(ctx):
  ''' hi()
  Basic response handler
  '''
  if ctx.channel.name in B.ALL:
    await ctx.send(Early.hi())

@bot.command(name='hello')
async def hello_there(ctx, *args):
  ''' hello_there(args)
  Responds with memeable quote. Note that args is there simply to allow users to type the \'there\'.
  '''
  if ctx.channel.name in B.GEN:
    outputs = Early.hello_there()
    for line in outputs:
      await ctx.send(line)

@bot.command(name='roll')
async def roll(ctx, *args):
  ''' roll(n)
  Rolls the given sets of dice and displays output iteratively. Rolls are organised into combos of the form ndm, for n rolls of dice with m sides for positive integral n and a value of m valid for dice in DnD. Responds to invalud combinations with a specialised response line.
  '''
  # print (ctx.channel, type(ctx.channel.name), ctx.channel.name == 'casino-night', ctx.channel is 'casino-night')
  if ctx.channel.name == B.BOT_GAMES[1]: # Restricts channel response
    outputs = await Happy.roll(args)
    for line in outputs:
      await ctx.send(line)

@bot.command(name='analysis')
async def analysis(ctx, *args):
  ''' analysis(args)
  Takes the list of optional args and kwargs that are provided and returns output describing the args, kwargs, and their values and number.
  '''
  if ctx.channel.name in B.TEXT[0]:
    analysis_outputs = await Early.analysis(ctx, args)
    # print(analysis_outputs)
    outputs = analysis_outputs[0]
    for line in outputs:
      await ctx.send(line)

@bot.command(name='scan')
async def scan(ctx, node='/'):
  ''' scan(node=dir)
  Takes a directory node of origin and outputs the files and folders within that node. Incomplete
  '''
  if ctx.channel.name in B.ALL:
    outputs = Happy.scan(node)
    for line in outputs:
      await ctx.send(line)

@bot.command(name='dex')
async def dex(ctx, *args):
  ''' dex(args)
  Overarching command for the Pokedex class and ops. Optional args correspond to specific commands within dex as well as arguments for these specific commands.
  '''
  if ctx.channel.name in B.BOT_GAMES[2]:
    if args[0] == 'list' and len(args) == 1:
      outputs = await Poke.open()
    elif args[0] == 'add' in args and len(args) == 2:
      outputs = await Poke.add(args[1])
    elif args[0] == 'delete':
      outputs = await Poke.delete(args[1])
    elif args[0] == 'clear':
      outputs = Poke.clear()
    else:
      await ctx.send('Invalid Pokédex operation.')
      return
    
    for line in outputs:
      await ctx.send(line)

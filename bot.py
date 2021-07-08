import os
import json
import data
import discord
import threading
import asyncio

from time import sleep
from discord.ext import commands

config = data.config()
bot = commands.Bot(command_prefix=config.get('prefix'))
bot.remove_command("help")
 
basedir = os.path.abspath(os.path.dirname(__file__))

async def presence():
    while True:
        presence_list=[config.get('name'),"For help: {}help".format(config.get('prefix'))]
        for presence_item in presence_list:
            await bot.change_presence(activity=discord.Activity(application_id=2,type=3,name=presence_item+"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"))
            await asyncio.sleep(10)

@bot.event
async def on_ready():
    print('Logged in as',bot.user.name)
    print(bot.user.id)
    print('===========')
    os.environ["botName"] = str(bot.user.name)
    os.environ["botId"] = str(bot.user.id)
    os.environ["botAvatar"] = str(bot.user.avatar_url)
    await presence()

for file in os.listdir("cmds"):
     if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cmds.{name}")
        

bot.run(config.get('token'))

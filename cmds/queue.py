import discord
import data as file 
from discord.ext import commands
from time import sleep
from embed_ui import embed, bot_base
import os
import sqlite3
import json

def get_data(data):
    return json.load(open("json/message.json",'r'))[data]
    
def set_data(key, data):
    try:
        datas = json.load(open("json/message.json",'r'))
    except:
        datas = {}
    with open("json/message.json",'w+') as f_data:
        datas[key] = data
        json.dump(datas, f_data)

class Queue(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        print('queue')
        
    async def admin(ctx):
        if type(ctx.channel) == discord.TextChannel:
            if ctx.message.author.guild_permissions.administrator:
                await ctx.message.delete()
                return True
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if int(get_data("message_id")) == reaction.message.id and str(reaction) == get_data("reaction") \
            and not user.bot:
            file.queue(user)
            
    @commands.command()
    @commands.check(admin)
    async def start(self, ctx):
        try:
            os.mkdir("json/queue")
        except:
            pass
        message = await ctx.send("",embed=embed())
        await message.add_reaction(get_data("reaction"))
        set_data("message_id",message.id)
        if "time" in json.load(open("json/message.json",'r')):
            await message.delete(delay=float(get_data("time"))*60)
        # else:
        #     await asyncio.sleep(10)
        
    @commands.command()
    @commands.check(admin)
    async def stop(self, ctx):
        await ctx.send("queue stoped")
        set_data("message_id","0")
    
    # setup [server] [channel]
    @commands.command()
    @commands.check(admin)
    async def setup(self, ctx):
        data = ctx.message.content.split(" ")
        if len(data) == 1:
            server = ctx.message.guild.id
            channel = ctx.message.channel.id
        else:
            server = data[1]
            channel = data[2]
        set_data("server",str(server))
        set_data("channel",str(channel))
        
    # set [time(mins)] {"title":"","description":"", "thumbnail"="", "img"="", "footer"="","author":{"name":"","icon_url":"","url":""}} reaction
    @commands.command()
    @commands.check(admin)
    async def set(self, ctx):
        data = ctx.message.content.split(" ")
        time = data[1]
        message = data[2]
        reaction = data[3]
        set_data("time",str(time))
        set_data("reaction",str(reaction))
        with open("json/message_body.json","w+") as f_data:
            f_data.write(message)
    
    @commands.command()
    @commands.check(admin)
    async def list(self, ctx):
        queues = file.data("queue")
        await ctx.author.create_dm()
        send = bot_base("**Queue List**\n", "")
        for row in queues.dirs():
            for key, datas in queues.load(row).items():
                send.add_field(name=key, value=datas['user'], inline=False)
                if int(key) % 10 == 0:
                    await ctx.author.dm_channel.send("",embed=send)
                    send = bot_base("", "")
                
    @commands.command()
    @commands.check(admin)
    async def reset(self, ctx):
        import shutil
        shutil.rmtree('json/queue')
        
    @commands.command()
    @commands.check(admin)
    async def help(self, ctx):
        await ctx.author.create_dm()
        prefix = file.config().get('prefix')
        if type(ctx.channel) == discord.TextChannel:
            server = ctx.channel.guild
            embed = bot_base("指令說明","[可選填]", footer=server.name,
                author={"name":os.environ["botName"],"icon_url":os.environ["botAvatar"]})
        else:
            embed = bot_base("指令說明","[可選填]", 
                author={"name":os.environ["botName"],"icon_url":os.environ["botAvatar"]})
        for command_type, command_list in file.help_data().items():
            embed.add_field(name="⠀", value=f"**{command_type}**", inline=False)
            for command, description in command_list.items():
                embed.add_field(name=f"`{prefix}{command}`", value=description, inline=True)
        await ctx.author.dm_channel.send("",embed=embed)
    
def setup(bot):
	bot.add_cog(Queue(bot))


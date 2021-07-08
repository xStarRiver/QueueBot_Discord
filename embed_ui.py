import discord
import data
import os
import json

config = data.config()

def base(title: str, description: str, color = config.get('color'), img="", footer=""):
    embed = discord.Embed(title=title,description=description,color=color)
    embed.set_image(url=img)
    embed.set_footer(text="{} {}".format(
        config.get('name'),footer), 
        icon_url=os.environ["botAvatar"])
    return embed

def bot_base(title: str, description: str, thumbnail="", img="", footer="",\
    author={"name":"","icon_url":"","url":""}, color = config.get('color')):
    embed = base(title, description, img=img, footer=', '+footer,color=color)
    if "url" in author.keys() :
        embed.set_author(name=author["name"], icon_url=author["icon_url"],url=author["url"])
    else:
        embed.set_author(name=author["name"], icon_url=author["icon_url"])
    embed.set_thumbnail(url=thumbnail)
    return embed
    
def embed():
    data = json.load(open("json/message_body.json",'r'))
    return bot_base(data["title"], data["description"], thumbnail=data["thumbnail"], \
       img= data["img"], footer=data["footer"],\
    author=data["author"], color = config.get('color'))

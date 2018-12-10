import sys 
sys.path.append('../')
import asyncio
from discord import Game
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import Parsing_modules.Bsoup_response as Bsoup_response  

BOT_PREFIX = "?"
TOKEN = ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
description = "UNIST Frame Data Bot"
bot = commands.Bot(command_prefix = BOT_PREFIX, description = description)
shorthand_dictionary = {"Yuzu" : "Yuzuriha", "Gord":"Gordeau", "Merk":"Merkava", "Bikehorn": "Nanase"}
move_info = None

#coroutine that sets the bot's status on startup. Print function will not respond until a yeild or send command is executed
@bot.event 
async def on_ready():
    print("Logged in as " + bot.user.name)
    await bot.change_presence(game=Game(name="UNIST"))

@bot.event
async def on_message(message):
    #Prevents the bot from responding to itself
    if message.author.bot:
        return
    
    #command structure ![character] [input notation]
    if message.content.startswith('!'):
        input_message = message.content.replace("!",'')
        message_as_cmd_list = input_message.split(' ',1)
        character = str(message_as_cmd_list[0].lower().capitalize())
        input = str(message_as_cmd_list[1].upper()).replace("J", "j")
        url_root = "http://wiki.mizuumi.net/w/Under_Night_In-Birth/UNIST/{}"
        try:
            #the system attempts to use the nickname first, if the nickname does not exist then the try function will catch the error and use the full inputted character
            response = Bsoup_response.get_HTML_requests(url_root.format(shorthand_dictionary[character]))
        except:
            response = Bsoup_response.get_HTML_requests(url_root.format(character))
        #the style of notation from normal to specials is different so it runs two separate functions
        if(Bsoup_response.is_normal(input)):
            move_info = Bsoup_response.find_normal(response, input)
        else:
            move_info = Bsoup_response.find_special(response, input)
        #formats data into a discord code block
        await bot.send_message(message.channel, "```{:20s}{:20s}\n{:20s}{:20s}\n{:20s}{:20s}\n{:20s}{:20s}\n{:20s}{:20s}\n{:20s}{:20s}\n{:20s}{:20s}```".
                                                format("Damage", move_info[0], "Startup", move_info[1], "Active", move_info[2], "Recovery", move_info[3],
                                                       "Frame Advantage", move_info[4], "Cancels", move_info[5], "Guard", move_info[6]))
    await bot.process_commands(message)
    

bot.run(TOKEN)

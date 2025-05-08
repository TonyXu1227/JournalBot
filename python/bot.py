# bot.py
import os
import datetime
import random
import discord
from rich import print
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()
f = open("/Users/bigricce1227/Documents/Coding_Projects/Tokens_and_Keys/JournalBot_Token", "r")
TOKEN = f.read()
#print(TOKEN)
client = commands.Bot(command_prefix = "!", intents=discord.Intents.all())

startList = [".START_JOURNAL", ".START_LOG", ".START_ENTRY", ".START_JOURNALING", ".NEW_ENTRY", ".NEW_LOG"]
endList = [".END_JORNAL", ".END_LOG", ".END_ENTRY", ".STOP_JOURNALING", ".STOP_ENTRY"]
readList = [".READ"]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')
    try:
        synced = await client.tree.sync()
        print("Synced up!")
    except Exception as e:
        print(e)

f = open("filepath.txt", "r")
basePath = f.read()
print(basePath)
f.close()

isJournaling = False
@client.event
async def on_message(message):
    global isJournaling
    global time
    global f
    if message.author == client.user:
        return
    if message.content.upper()[0:5] in readList and not(isJournaling):
        #read from file
        date = message.content[6:]
        print(date)
        f = open((basePath+date), "r")
        content = f.read()
        await message.channel.send("Entry on " + date)
        await message.channel.send(content)
        print("read entry")
    argspace = message.content.find(" ")
    if message.content.upper()[:argspace] in startList and not(isJournaling):
        await message.channel.send("What is on the mind?")
        now = datetime.datetime.now()
        isJournaling = True
        title = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        cont = message.content
        if argspace != 0:
            print("cust")
            title = cont[argspace+1:]
        f = open((basePath+title), "w")
        if f.closed:
            print ("file opened unsuccessfully")
        else:
            print("started entry: " + title)
    elif isJournaling:
        if message.content.upper() in endList:
            await message.channel.send("What a day!")
            isJournaling = False
            f.close()
            f = None
            print("ended entry")
        else:
            #write to file
            f.write(message.content + "\n-----\n")
            now = datetime.datetime.now()
            print(now)
            print("wrote into entry")
        
    print("message delivered: " + message.content)

@client.tree.command(name = "read")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"responded to {interaction.user.mention}", ephemeral = True)

client.run(TOKEN)

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
    global query
    global title
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
        #print(content)
        await message.channel.send("Entry on " + date)
        iterator = int(len(content)/1995)+1
        print(iterator)
        for i in range(iterator):
            start = i*1998
            end = min(len(content), ((i+1)*1995))
            payload = content[start: end] + "-->"
            await message.channel.send(payload)
        print("read entry")
    argspace = message.content.find(" ")

    #start an entry
    if (message.content.upper()[:argspace] in startList) or (message.content.upper() in startList) and not(isJournaling):
        now = datetime.datetime.now()
        cont = message.content
        if argspace != 0:
            print("cust")
            title = cont[argspace+1:]
        if message.content.upper() in startList:
            title = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        if os.path.exists(basePath+title):
            print("file already exists!!")
            query = -1
            await message.channel.send("That file exists! would you like to continue? (Type \"C\" to continue)")
        else:
            isJournaling = True
            await message.channel.send("What is on the mind?")
            f = open((basePath+title), "w")
            if f.closed:
                print ("file opened unsuccessfully")
            else:
                print("started entry: " + title)
    # end an entry
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
    elif query == -1:
        if message.content != "C":
            query = 0
        else:
            isJournaling = True
            await message.channel.send("What is on the mind?")
            f = open((basePath+title), "w")
            if f.closed:
                print ("file opened unsuccessfully")
            else:
                print("started entry: " + title)
        
    print("message delivered: " + message.content + " ")
    print(query)

@client.tree.command(name = "read")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"responded to {interaction.user.mention}", ephemeral = True)

client.run(TOKEN)

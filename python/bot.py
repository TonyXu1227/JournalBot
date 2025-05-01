# bot.py
import os
import time
import random
import discord
from rich import print
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
#print(TOKEN)
client = commands.Bot(command_prefix = "!", intents=discord.Intents.all())

startList = [".START_JOURNAL", ".START_LOG", ".START_ENTRY", ".START_JOURNALING", ".NEW_ENTRY", ".NEW_LOG"]
endList = [".END_JORNAL", ".END_LOG", ".END_ENTRY", ".STOP_JOURNALING", ".STOP_ENTRY"]
readList = ["READ FROM"]


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')
    try:
        synced = await client.tree.sync()
        print("Synced up!")
    except Exception as e:
        print(e)

isJournaling = False
@client.event
async def on_message(message):
    global isJournaling
    global time
    if message.author == client.user:
        return
    if message.content.upper()[0:8] in readList and not(isJournaling):
        #read from file
        now = time.gmtime()
        print("read entry")
    if message.content.upper() in startList and not(isJournaling):
        await message.channel.send("What is on the mind?")
        print("started entry")
        isJournaling = True
    if isJournaling:
        if message.content.upper() in endList:
            await message.channel.send("What a day!")
            isJournaling = False
            print("ended entry")
        else:
            #write to file
            now = time.gmtime()
            print("wrote entry")


        
    print("message delivered: " + message.content)

@client.tree.command(name = "read")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"responded to {interaction.user.mention}", ephemeral = True)

client.run(TOKEN)
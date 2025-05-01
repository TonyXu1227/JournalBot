# bot.py
import os
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

isJournaling = False
startList = ["START JOURNAL", "START_LOG", "START ENTRY", "START JOURNALING", "NEW ENTRY", "NEW LOG"]
endList = ["END JORNAL", "END LOG", "END ENTRY", "STOP JOURNALING", "STOP ENTRY"]
readList = ["READ FROM"]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')
    try:
        synced = await client.tree.sync()
        print("Synced up!")
    except Exception as e:
        print(e)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.upper()[0:8] in readList and not(isJournaling):
        #read from file
        now = time.gmtime()
        print("read entry")
    if message.upper() in startList and not(isJournaling):
        await message.channel.send("What is on the mind?")
        print("started entry")
        isJournaling = True
    if isJournaling:
        if message.upper() in endList:
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
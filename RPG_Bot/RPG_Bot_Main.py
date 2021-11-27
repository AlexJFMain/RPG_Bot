import os
import discord
import datetime
import random
import json
import math

from pytz import timezone
from time import sleep
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv
from pathlib import Path

init(convert=True)

# Discord API Token, stored in .env in same directory.
#-----------------------------------------------------------------
load_dotenv()
discordApiToken = os.getenv("API_TOKEN")
#-----------------------------------------------------------------

# Constants.
#-----------------------------------------------------------------
discordTimeZone = timezone('US/Eastern')
#-----------------------------------------------------------------

# Establish console colors.
#-----------------------------------------------------------------
class consoleColors:
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKRED = '\033[91m'
    OKCYAN = '\033[96m'
    OKMAGENTA = '\033[95m'
    OKWHITE = '\033[37m'

    HEADER = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#-----------------------------------------------------------------

client = discord.Client()

# Assorted helper methods.
#-----------------------------------------------------------------
##################################################################
#-----------------------------------------------------------------
def logEvent(* stringInputs):
    finalString = ""
    for inputData in stringInputs:
        finalString += str(inputData)
    print("%s : %sEVENT%s - %s%s%s" % (datetime.datetime.now(discordTimeZone).strftime("%Y-%m-%d %H:%M:%S %p"), 
    consoleColors.OKGREEN, consoleColors.ENDC, consoleColors.BOLD, finalString, consoleColors.ENDC))
#-----------------------------------------------------------------
def logError(* stringInputs):
    finalString = ""
    for inputData in stringInputs:
        finalString += str(inputData)
    print("%s : %sERROR%s - %s%s%s" % (datetime.datetime.now(discordTimeZone).strftime("%Y-%m-%d %H:%M:%S %p"), 
    consoleColors.OKYELLOW, consoleColors.ENDC, consoleColors.BOLD, finalString, consoleColors.ENDC))
#-----------------------------------------------------------------
def logAlert(* stringInputs):
    finalString = ""
    for inputData in stringInputs:
        finalString += str(inputData)
    print("%s : %sALERT%s - %s%s%s" % (datetime.datetime.now(discordTimeZone).strftime("%Y-%m-%d %H:%M:%S %p"), 
    consoleColors.OKRED, consoleColors.ENDC, consoleColors.BOLD, finalString, consoleColors.ENDC))
#-----------------------------------------------------------------
def rollDie(sides):
    return random.randint(1, sides)
#-----------------------------------------------------------------
def rollDice(quantity, sides):
    quantityOfDie = quantity
    arr = []
    for i in range (1, quantityOfDie + 1):
        arr.append(rollDie(sides))
        sleep(0.01*random.randint(1, 10))
    arr.sort()
    return arr
#-----------------------------------------------------------------
def createEmbed(description, username, icon, color, inline, *content):
    embed_read = discord.Embed(description = description , color = color)
    embed_read.set_author(name = username, icon_url = icon)
    for items in content:
        try:
            embed_read.add_field(name = items["title"], value = items["description"], inline = inline)
        except Exception as e:
            logError('\'', e, f"\' thrown by \'createEmbed\' call on data: \'{{{items}}}\'")
    return embed_read
#-----------------------------------------------------------------
def getModifier(score):
    return "+" + str(int(math.floor((score - 10)/2))) if int(math.floor((score - 10)/2)) > 0 else int(math.floor((score - 10)/2))
#-----------------------------------------------------------------
##################################################################
#-----------------------------------------------------------------

@client.event   
async def on_ready():
    logEvent(client.user, ' has connected to Discord!')

@client.event
async def on_message(message):

    # Access handling.
    #-----------------------------------------------------------------
    ##################################################################
    #-----------------------------------------------------------------
    # Will not reference self.
    if message.author == client.user:
        return
    #-----------------------------------------------------------------
    # Break off if not accessing a function.
    if not message.content.startswith('!'):
        return
    #-----------------------------------------------------------------
    # Easy access dictionary for data from message.
    messageDict = {
        "channelID": message.channel.id,
        "channelName": message.channel.name,
        "messageID": message.author.id,
        "messageName": message.author.name,
        "messageNick": message.author.nick,
        "messageIcon": message.author.avatar_url,
        "messageRoles": message.author.roles,
        "messageContent": message.content
    }
    messageAlias = messageDict['messageNick'] if messageDict['messageNick'] is not None else messageDict['messageName']
    #-----------------------------------------------------------------
    ##################################################################
    #-----------------------------------------------------------------

    # Log messages in proper formatting
    #-----------------------------------------------------------------
    def logMessage(* stringInputs):
        alias = messageAlias 
        id = messageDict['messageID']
        finalString = ""
        for inputData in stringInputs:
            finalString += str(inputData)
        print("%s : %sMSG  %s - %s%s%s%s%s" % (datetime.datetime.now(discordTimeZone).strftime("%Y-%m-%d %H:%M:%S %p"), 
        consoleColors.OKMAGENTA, consoleColors.ENDC, consoleColors.BOLD, 
        'ALIAS: \'' + consoleColors.OKCYAN + str(alias) + consoleColors.OKWHITE, 
        '\' ID: \'' + consoleColors.OKCYAN + str(id) + consoleColors.OKWHITE + '\' ', 
        finalString, consoleColors.ENDC))
    #-----------------------------------------------------------------
        
    # Commands for calling by standard users.
    #-----------------------------------------------------------------
    ##################################################################
    #-----------------------------------------------------------------
    if message.content.startswith('!info'):
        logMessage("called \'!info\'")
        infoString = ""

        infoString += "**!roll <quantity> <sides>**\
        \n> __Description__: Returns a list of dice and their sum, based off your input values.\
        \n> __Default__: quantity = 1, sides = 20\
        \n> __Limit__: 1 <= quantity <= 20, 2 <= sides <= 100\
        \n> __Example__: *\"!roll 3 100\"* rolls 3d100\
        \n"

        infoString += "**!template**\
        \n> __Description__: Returns a template JSON file for D&D Character Sheet.\
        \n"

        infoString += "**!getFile**\
        \n> __Description__: Returns a JSON file for your character sheet. If you do not have one you can use '!setFile' to create one.\
        \n"

        infoString += "**!setFile**\
        \n> __Description__: Creates a JSON file for you character sheet, if it already exists this call can be used to overwrite the files contents.\
        \n> __Example__: *\"!setFile {\"Character Name\":\"Walter\"}\"* overwites file with the content *\"{\"Character Name\":\"Walter\"}\"*\
        \n"

        infoString += "**!getStats**\
        \n> __Description__: Retrieves stats from your JSON file.\
        \n"

        await message.channel.send(infoString)

        return
    #-----------------------------------------------------------------
    if message.content.startswith('!template'):

        logMessage("called \'!template\'")

        try:
            await message.channel.send("**Character Sheet JSON Template:**\n", file=discord.File("chSheets\\template.json"))
        except Exception as e:
            logError('\'', e, "\' thrown by \'!template\' call")

        return
    #-----------------------------------------------------------------
    if message.content.startswith('!roll'):
        messageArr = message.content.split(" ")
        quantity = 1
        sides = 20

        try:
            quantity = int(messageArr[1])
        except Exception as e:
            logError('\'', e, "\' thrown by \'!roll\' call on value \'quantity\'")

        try:
            sides = int(messageArr[2])
        except Exception as e:
            logError('\'', e, "\' thrown by \'!roll\' call on value \'sides\'")

        if(quantity < 1 or quantity > 20):
            quantity = 1
        if(sides < 2 or sides > 100):
            sides = 20

        rollResult = rollDice(quantity, sides)
        logMessage("called \'!roll\' for ", quantity, "d", sides)

        data0 = {
            "title": "Result:",
            "description": rollResult
        }

        data1 = {} if quantity == 1 else {
            "title": "Sum:",
            "description": sum(rollResult, 0)
        }

        await message.channel.send(embed = createEmbed(f"**Dice Roll** - {quantity}d{sides}", messageAlias, messageDict["messageIcon"], 0xffb957, False, data0, data1))

        return
    #-----------------------------------------------------------------
    if message.content.startswith('!getFile'):
        path = Path(f"chSheets\\charSheetUserID{messageDict['messageID']}.json")
        exists = path.is_file()

        logMessage("called \'!getFile\'")

        if(exists):
            logEvent(f"File \'{path}\' retrieved with \'!getFile\'")
            await message.channel.send(f"Character Sheet JSON for **{messageAlias}**...\n", file=discord.File(path))
        else:
            logEvent(f"Attempted retrieval of \'{path}\' via \'!getFile\', file does not exist")
            await message.channel.send(f"Character Sheet JSON __does not__ exist for **{messageAlias}**...")

        return
    #-----------------------------------------------------------------
    if message.content.startswith('!setFile'):
        path = Path(f"chSheets\\charSheetUserID{messageDict['messageID']}.json")
        exists = path.is_file()
        trimmedMsg = message.content[8:]

        logMessage(f"called \'!setFile\' with content \'{trimmedMsg}\'")

        if(not exists):
            logEvent(f"Current character sheet does not exist, file \'{path}\' has been created")
            newJSONFile = open(path, "w")

        try:
            open(path, "w").close()
            with open(path, "a") as writeFile:
                for line in trimmedMsg:
                    writeFile.write(line)
        except Exception as e:
            logAlert('\'', e, f"\' thrown by \'!setFile\' call while writing to {path} with message content")

        return
    #-----------------------------------------------------------------
    if message.content.startswith('!getStats'):
        path = Path(f"chSheets\\charSheetUserID{messageDict['messageID']}.json")
        exists = path.is_file()

        logMessage("called \'!getStats\'")

        if(exists):
            try:
                file = open(path, "r")
                data = json.loads(file.read())

                charName = data["Details"]["Character Name"]
                charProf = data["Stats"]["Prof Bonus"]
                charPerc = data["Stats"]["Passive Perception"]
                charThro = data["Stats"]["Saving Throws"]
                charSkil = data["Stats"]["Skills"]

                strStat = {
                    "title": "Strength:",
                    "description": "%s (%s)"%(data["Stats"]["Str"], getModifier(data["Stats"]["Str"]))
                }
                dexStat = {
                    "title": "Dexterity:",
                    "description": "%s (%s)"%(data["Stats"]["Dex"], getModifier(data["Stats"]["Dex"]))
                }
                conStat = {
                    "title": "Constitution:",
                    "description": "%s (%s)"%(data["Stats"]["Con"], getModifier(data["Stats"]["Con"]))
                }
                wisStat = {
                    "title": "Wisdom:",
                    "description": "%s (%s)"%(data["Stats"]["Wis"], getModifier(data["Stats"]["Wis"]))
                }
                intStat = {
                    "title": "Intelligence:",
                    "description": "%s (%s)"%(data["Stats"]["Int"], getModifier(data["Stats"]["Int"]))
                }
                chaStat = {
                    "title": "Charisma:",
                    "description": "%s (%s)"%(data["Stats"]["Cha"], getModifier(data["Stats"]["Cha"]))
                }

                await message.channel.send(embed = createEmbed(f"**Character Stats:** {charName}\
                \n\
                \n**Proficiency Bonus:** {charProf}\
                \n**Saving Throws:**: {charThro}\
                \n**Skills:**: {charSkil}\
                \n**Passive Perception:** {charPerc}\
                \n",
                messageAlias, messageDict["messageIcon"], 0x4265ed, False, 
                strStat, dexStat, conStat, wisStat, intStat, chaStat))

                file.close()
            except Exception as e:
                logError('\'', e, f"\' thrown by \'!getStats\' call on {path}")
                await message.channel.send(f"Could __not__ retrieve stats for **{messageAlias}**...")
        else:
            await message.channel.send(f"Could __not__ retrieve stats for **{messageAlias}**...")

        return
    #-----------------------------------------------------------------
    ##################################################################
    #-----------------------------------------------------------------

client.run(discordApiToken)
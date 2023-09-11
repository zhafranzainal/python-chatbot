# pip install googletrans==4.0.0rc1
# alternative lib: pip install google-cloud-translate==2.0.1

import os
import discord

from keep_alive import keep_alive
from googletrans import Translator


# common language codes:-
# ar: Arabic
# bn: Bengali
# zh-cn: Chinese (Simplified)
# en: English
# tl: Filipino
# fr: French
# de: German
# id: Indonesian
# it: Italian
# ja: Japanese
# ko: Korean
# ms: Malay
# ru: Russian
# es: Spanish
# ta: Tamil
# vi: Vietnamese

def get_translation(message):
    translator = Translator()
    translated = translator.translate(message, dest="en")
    return translated.text


# get default set of intents then enable intent to receive message content
permissions = discord.Intents.default()
permissions.message_content = True

# represent bot
client = discord.Client(intents=permissions)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    # send message to each server it belongs to
    for guild in client.guilds:
        channel = guild.system_channel
        await channel.send(f"{client.user} is online!")


@client.event
async def on_message(message):
    # skip messages from the bot itself
    if message.author == client.user:
        return

    print(message.content)

    translator = Translator()
    detected_language = translator.detect(message.content).lang

    if message.content.startswith("!"):

        # split message into list using "!" as the separator
        text = message.content.split("! ")

        # explicitly convert text in the list to string
        string_text = map(str, text)

        # concatenate the list of strings into a single string
        list_to_str = "".join(string_text)

        if detected_language == "en":
            await message.channel.send(list_to_str)
        else:
            translated = get_translation(list_to_str)
            await message.channel.send(translated)


keep_alive()

# run bot using TOKEN from env
client.run(os.environ['TOKEN'])

# pip install googletrans==4.0.0rc1
# alternative lib: pip install google-cloud-translate==2.0.1

import os
import discord

from keep_alive import keep_alive
from googletrans import Translator

'''
common language codes:-
ar: Arabic
bn: Bengali
zh-cn: Chinese (Simplified)
en: English
tl: Filipino
fr: French
de: German
id: Indonesian
it: Italian
ja: Japanese
ko: Korean
ms: Malay
ru: Russian
es: Spanish
ta: Tamil
vi: Vietnamese
'''

BOT_PREFIX = "!"  # bot's command prefix
DEST_LANG = "en"  # destination language for translation

translator = Translator()


def get_translation(message):
    translated = translator.translate(message, dest=DEST_LANG)
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

    if message.content.startswith(BOT_PREFIX):

        # better alternative: extract text without prefix
        # list_to_str = message.content[len(BOT_PREFIX):]

        # split message into list using BOT_PREFIX as the separator
        text = message.content.split(BOT_PREFIX + " ")

        # explicitly convert text in the list to string
        string_text = map(str, text)

        # concatenate the list of strings into a single string
        list_to_str = "".join(string_text)

        detected_language = translator.detect(list_to_str).lang

        if detected_language == DEST_LANG:
            await message.channel.send(list_to_str)
        else:
            translated = get_translation(list_to_str)
            await message.channel.send(translated)


keep_alive()

# run bot using TOKEN from env
client.run(os.environ['TOKEN'])

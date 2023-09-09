import json
import os

import discord
import requests

from keep_alive import keep_alive


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = '"' + json_data[0]['q'] + '" - ' + json_data[0]['a']

    return quote


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
    if message.content.lower().startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)


keep_alive()

# Run bot using TOKEN from env
client.run(os.environ['TOKEN'])

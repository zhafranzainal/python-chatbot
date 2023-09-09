import os

import discord

# get default set of intents then enable intent to receive message content
permissions = discord.Intents.default()
permissions.message_content = True

# represent bot
client = discord.Client(intents=permissions)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    # check if the message is from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith("Hello"):
        await message.channel.send("Hello!")


# Run bot using TOKEN from env
client.run(os.environ['TOKEN'])

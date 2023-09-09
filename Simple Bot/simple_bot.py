import os

import discord

# get full or relative path to file
hello_gif_path = os.path.join(os.path.dirname(__file__), 'hello.gif')

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
    # check if the message is from the bot itself
    if message.author == client.user:
        return

    if message.content.lower().startswith("hello"):
        await message.channel.send("Hello!", file=discord.File(hello_gif_path))


# Run bot using TOKEN from env
client.run(os.environ['TOKEN'])

import os
import discord

from keep_alive import keep_alive

# get default set of intents then enable intent to receive message content
permissions = discord.Intents.default()
permissions.message_content = True

# create bot
bot = discord.Client(intents=permissions)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # send message to each server the bot belongs to
    for guild in bot.guilds:
        channel = guild.system_channel
        await channel.send(f"{bot.user} is online!")


@bot.event
async def on_message(message):
    if message.content.lower().startswith("$hello"):
        await message.channel.send(
            "Hello! \nWelcome to Meal Recommender System \n "
            "$breakfast / $lunch / $dinner \n "
            "1: food / 2: snack \n "
            "e.g.: $breakfast 2"
        )

    elif message.content.lower().startswith("$breakfast"):

        text = message.content.split("$breakfast ")
        list_to_str = "".join(map(str, text))

        if int(list_to_str) == 1:
            choice = "sandwich"
        else:
            choice = "salad"

    elif message.content.lower().startswith("$lunch"):

        text = message.content.split("$lunch ")
        list_to_str = "".join(map(str, text))

        if int(list_to_str) == 1:
            choice = "spaghetti"
        else:
            choice = "tacos"

    elif message.content.lower().startswith("$dinner"):

        text = message.content.split("$dinner ")
        list_to_str = "".join(map(str, text))

        if int(list_to_str) == 1:
            choice = "sushi"
        else:
            choice = "french fries"

    recommendation = "Food recommendation: " + choice

    # get full or relative path to file
    food_image_path = os.path.join(os.path.dirname(__file__), f'Images/{choice}.png')

    await message.channel.send(recommendation)
    await message.channel.send(file=discord.File(food_image_path))


keep_alive()

# run bot using TOKEN from env
bot.run(os.environ['TOKEN'])

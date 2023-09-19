import os
import discord

from keep_alive import keep_alive

# define a dictionary that maps meals to their corresponding food choices
MEAL_CHOICES = {
    "$breakfast": ["sandwich", "salad"],
    "$lunch": ["spaghetti", "tacos"],
    "$dinner": ["sushi", "french fries"],
}

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
    text = message.content.lower()

    if text.startswith("$hello"):
        response = "Hello!\n> Welcome to Meal Recommender System\n> " \
                   "$breakfast / $lunch / $dinner\n> " \
                   "1: food / 2: snack\n> " \
                   "e.g.: $breakfast 2"

        await message.channel.send(response)

    for meal, choices in MEAL_CHOICES.items():

        if text.startswith(meal):
            choice_number = text.split(meal)[-1].strip()

            try:
                choice = choices[int(choice_number) - 1]
            except (ValueError, IndexError):
                choice = "Invalid choice. Please use 1 or 2."

            recommendation = "Food recommendation: " + choice

            # get full or relative path to file
            food_image_path = os.path.join(os.path.dirname(__file__), f'Images/{choice}.png')

            await message.channel.send(recommendation)
            await message.channel.send(file=discord.File(food_image_path))


keep_alive()

# run bot using TOKEN from env
bot.run(os.environ['TOKEN'])

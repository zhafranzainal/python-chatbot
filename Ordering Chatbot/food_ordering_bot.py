import os
import discord

from keep_alive import keep_alive

# create default set of intents then enable intent to receive message content
permissions = discord.Intents.default()
permissions.message_content = True

# create bot
bot = discord.Client(intents=permissions)

# define a dictionary (tuples) that maps keys to their corresponding food names and prices
FOOD_CHOICES = {
    1: ("Pizza", 15),
    2: ("Spaghetti Carbonara", 10),
    3: ("Spaghetti Aglio e Olio", 8),
}

choice = ""
quantity = ""


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # send message to each server the bot belongs to
    for guild in bot.guilds:
        channel = guild.system_channel
        await channel.send(f"{bot.user} is online!")


@bot.event
async def on_message(message):
    # skip messages from the bot itself
    if message.author == bot.user:
        return

    if message.content.lower().startswith("$hello"):
        response = "Hello!\n> Welcome to Pizza Hub\n> " \
                   "What's your name?\n> " \
                   "Type $name [your name]"

        await message.channel.send(response)

    elif message.content.lower().startswith("$name"):
        name = message.content.split("$name ")
        text = "".join(map(str, name))

        menu = f"Hello {text}, what do you want to eat?\n> "

        for key, (food_name, food_price) in FOOD_CHOICES.items():
            menu += f"{key}. {food_name.ljust(25)} RM{food_price}\n> "

        menu += "e.g. $food 2"

        await message.channel.send(menu)

    elif message.content.lower().startswith("$food"):
        global choice
        food = message.content.split("$food ")
        text = "".join(map(str, food))

        choice_key = int(text)

        if choice_key in FOOD_CHOICES:
            choice = FOOD_CHOICES[choice_key][0]
            orders = f"How many {choice} do you want to order?\n> " \
                     "e.g. $qty 5"

        await message.channel.send(orders)

    elif message.content.lower().startswith("$qty"):
        global quantity
        qty = message.content.split("$qty ")
        quantity = "".join(map(str, qty))
        orders_final = f"Are you sure you want to buy {quantity} {choice}?\n> " \
                       "(y/n)"

        await message.channel.send(orders_final)

    elif message.content.lower().startswith("y"):

        for key, (food_name, food_price) in FOOD_CHOICES.items():

            if choice == food_name:
                price = food_price
                break

        total = price * int(quantity)

        bill = f"Your total bill is RM{total}.\n" \
               "Thank you for shopping with us!"

        await message.channel.send(bill)

    elif message.content.lower().startswith("n"):
        await message.channel.send("Okay, good bye!")

    else:
        await message.channel.send("Sorry, I don't understand")


keep_alive()

# run bot using TOKEN from env
bot.run(os.environ['TOKEN'])

import os
import discord

from keep_alive import keep_alive

# create default set of intents then enable intent to receive message content
permissions = discord.Intents.default()
permissions.message_content = True

# create bot
bot = discord.Client(intents=permissions)

food1 = "Pizza"
food2 = "Carbonara Pasta"
food3 = "Spaghetti Aglio e Olio"
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
        menu = f"Hello {text}, what do you want to eat?\n> " \
               "1. Pizza                    RM15\n> " \
               "2. Carbonara Pasta          RM10\n> " \
               "3. Spaghetti Aglio e Olio   RM8\n> " \
               "e.g. $food 2"

        await message.channel.send(menu)

    elif message.content.lower().startswith("$food"):
        global choice
        food = message.content.split("$food ")
        text = "".join(map(str, food))
        if int(text) == 1:
            choice = food1
        elif int(text) == 2:
            choice = food2
        elif int(text) == 3:
            choice = food3
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
        if choice == food1:
            price = 15
        elif choice == food2:
            price = 10
        elif choice == food3:
            price = 8

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

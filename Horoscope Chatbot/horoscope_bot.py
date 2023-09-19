import os
import discord
import requests

from bs4 import BeautifulSoup
from keep_alive import keep_alive

# define a dictionary that maps zodiac signs to their corresponding numbers
signs = {
    "aries": 1,
    "taurus": 2,
    "gemini": 3,
    "cancer": 4,
    "leo": 5,
    "virgo": 6,
    "libra": 7,
    "scorpio": 8,
    "sagittarius": 9,
    "capricorn": 10,
    "aquarius": 11,
    "pisces": 12,
}


class Horoscope:

    def __init__(self, current_date, description):
        self.current_date = current_date
        self.description = description


def get_horoscope(sign):
    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={signs.get(sign, '')}"

    # send HTTP request to fetch web page
    response = requests.get(url)

    # parse HTML content of the page
    html = BeautifulSoup(response.text, 'html.parser')

    # find element containing horoscope text
    container = html.find("p")

    # remove leading/trailing whitespace then split between dates and actual horoscope message
    split_message = container.text.strip().split(" - ")
    current_date = split_message[0]
    description = split_message[1]

    return Horoscope(current_date, description)


# get default set of intents then enable intent to receive message content
permissions = discord.Intents.default()
permissions.message_content = True

# create bot
bot = discord.Client(intents=permissions)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # send message to each server it belongs to
    for guild in bot.guilds:
        channel = guild.system_channel
        await channel.send(f"{bot.user} is online!")


@bot.event
async def on_message(message):
    if message.content.lower() in signs:
        sign = message.content.lower()
        horoscope = get_horoscope(sign)
        quote = f"Today's horoscope for {sign.title()}:\n> " \
                f"Current date: {horoscope.current_date}\n> \n> " \
                f"{horoscope.description}"

        await message.channel.send(quote)


keep_alive()

# run bot using TOKEN from env
bot.run(os.environ['TOKEN'])

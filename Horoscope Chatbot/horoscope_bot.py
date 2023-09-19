import os
import discord
import requests

from bs4 import BeautifulSoup

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


def get_horoscope(sign):
    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={signs.get(sign, '')}"

    # send HTTP request to fetch web page
    response = requests.get(url)

    # parse HTML content of the page
    html = BeautifulSoup(response.text, 'html.parser')

    # find element containing horoscope text
    container = html.find("p")

    # remove leading/trailing whitespace then split between dates and actual horoscope message
    horoscope_message = container.text.strip().split(" - ")[1]

    return horoscope_message


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
    if message.content.lower() in signs:
        sign = message.content.lower()
        quote = get_horoscope(sign)
        await message.channel.send(f"Here's today's horoscope for {sign.title()}:\n> \"{quote}\"")


# run bot using TOKEN from env
client.run(os.environ['TOKEN'])

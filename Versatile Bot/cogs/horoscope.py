import requests

from discord.ext import commands
from bs4 import BeautifulSoup

# Define a dictionary that maps zodiac signs to their corresponding numbers
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


class Horoscope(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="horoscope", description="Provides sign's daily horoscope")
    async def horoscope(self, ctx: commands.Context, sign: str):

        await ctx.defer(ephemeral=True)

        if not sign:
            await ctx.send("Please put in a sign!", ephemeral=True, delete_after=5)
            return
        elif sign.lower() not in signs.keys():
            await ctx.send("Please enter a valid sign!", ephemeral=True, delete_after=5)
            return

        url = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=" \
              + str(signs[sign.lower()])

        # Send HTTP request to fetch web page
        response = requests.get(url)

        # Parse HTML content of the page
        html = BeautifulSoup(response.text, 'html.parser')

        # Find element containing horoscope text
        container = html.find("p")

        # Remove leading/trailing whitespace then split between dates and actual horoscope message
        horoscope_message = container.text.strip().split(" - ")[1]

        await ctx.send(f"Here's today's horoscope for {sign.title()}:\n> \"{horoscope_message}\"", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Horoscope(bot))

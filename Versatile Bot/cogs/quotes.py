import requests
import json

from discord.ext import commands


class Quotes(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="quote", description="Gives a random quote", with_app_command=True)
    @commands.has_permissions(administrator=True)
    async def quote(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)

        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = f'"{json_data[0]["q"]}"\n> — {json_data[0]["a"]}'

        await ctx.send(f"Here's a quote:\n> {quote}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Quotes(bot))

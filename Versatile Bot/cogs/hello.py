from discord.ext import commands


class Hello(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="hello", description="Says hello", with_app_command=True)
    @commands.has_permissions(administrator=True)
    async def hello(self, ctx: commands.Context):
        # Defer the response to indicate the bot is working
        await ctx.defer(ephemeral=True)

        # Send hello message that's only visible to the user who triggered the command
        await ctx.send(f"Hello, {ctx.author}!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hello(bot))

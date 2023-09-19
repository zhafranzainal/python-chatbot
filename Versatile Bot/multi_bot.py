import os
import aiohttp
import discord
from discord.ext import commands
from keep_alive import keep_alive

# List of cogs (extensions) to load
cogs = ("hello", "quotes", "translate", "horoscope", "music")


class MultiBot(commands.Bot):

    def __init__(self):
        # Create a default set of intents then enable message content intent
        permissions = discord.Intents.default()
        permissions.message_content = True

        # Initialize bot
        super().__init__(command_prefix="!", intents=permissions, case_insensitive=True)

        # Initialize session
        self.session = None

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        # Create session for making HTTP requests
        self.session = aiohttp.ClientSession()

        # Send message to each server the bot belongs to
        for guild in self.guilds:
            channel = guild.system_channel
            await channel.send(f"{self.user} is online!")
            await self.tree.sync()

    async def setup_hook(self):
        for cog in cogs:
            await self.load_extension(f"cogs.{cog}")

    async def close(self):
        await super().close()
        await self.session.close()


bot = MultiBot()
# keep_alive()

# Run bot using TOKEN from env
bot.run(os.environ['TOKEN'])

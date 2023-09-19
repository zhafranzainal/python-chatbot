# pip install googletrans==4.0.0rc1
# alternative lib: pip install google-cloud-translate==2.0.1

import discord
import googletrans

from discord.ext import commands
from typing import Optional

gt_lang_keys = googletrans.LANGUAGES.keys()
translator = googletrans.Translator()


class Translate(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="translate", description="Translates text to a different language", aliases=["tr"])
    async def translate(self, ctx: commands.Context,
                        text_to_translate: str,
                        dest_lang: Optional[str] = "",
                        src_lang: Optional[str] = ""
                        ):

        await ctx.defer(ephemeral=True)

        if not text_to_translate:
            await ctx.send("Please put some text to translate!", ephemeral=True, delete_after=5)
            return

        if not dest_lang or dest_lang not in gt_lang_keys:
            # message += f"{dest_lang} is not a valid option. Translating to English...\n"
            dest_lang = "en"

        if not src_lang or src_lang not in gt_lang_keys:
            # message += f"{src_lang} is not a valid option. Detecting language...\n"
            src_lang = translator.detect(text_to_translate).lang

        if src_lang == dest_lang:
            await ctx.send("You're translating to the same language. Stop.", ephemeral=True, delete_after=5)
            return

        translated = translator.translate(text_to_translate, src=src_lang, dest=dest_lang).text

        embed = discord.Embed(title="Translate", description="Translating from {} to {}".format(
            googletrans.LANGUAGES[src_lang].title(),
            googletrans.LANGUAGES[dest_lang].title()
        ))

        embed.add_field(name="Original", value=text_to_translate, inline=False)
        embed.add_field(name="Translated", value=translated, inline=False)

        # message += f"Translating from {googletrans.LANGUAGES[src_lang].title()} \
        # to {googletrans.LANGUAGES[dest_lang].title()}...\n> **Original:** \
        # {text_to_translate}\n> **Translation:** {translated}"

        await ctx.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Translate(bot))

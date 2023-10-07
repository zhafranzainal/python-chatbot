# pip install PyNaCl
# https://ffmpeg.org/download.html

import discord
import asyncio
import yt_dlp

from discord.ext import commands
from youtube_search import YoutubeSearch


def embed_song(song_info):
    embed = discord.Embed(title=song_info['title'], url=song_info['page_url'])
    embed.set_author(name=song_info['uploader'])
    embed.set_image(url=song_info['thumbnail'])
    embed.add_field(name="Duration", value=song_info['duration'], inline=True)
    embed.add_field(name="Requested by", value=song_info['author'], inline=True)
    return embed


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.queue = []
        self.is_playing = False
        self.is_looping = False

    async def _play_next(self, voice_client: discord.VoiceClient, channel: discord.TextChannel, skip: bool):

        next_song = {}

        if not self.is_looping or skip:
            self.queue.pop(0)

        if self.queue:
            next_song = self.queue[0]
            embed = embed_song(next_song)

            next_source = await discord.FFmpegOpusAudio.from_probe(next_song['link'], **self.ffmpeg_options)

            await channel.send(embed=embed, delete_after=60)
            voice_client.play(next_source, after=lambda x=None: self._play_after(voice_client, channel))
        else:
            self.is_playing = False

    def _play_after(self, voice_client: discord.VoiceClient, channel: discord.TextChannel, skip: bool = False):

        coro = self._play_next(voice_client, channel, skip)
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)

        try:
            fut.result()
        except Exception:
            pass

    @commands.hybrid_command(name="join", description="Joins a voice channel (if not in one yet)")
    async def join(self, ctx: commands.Context):

        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.send("The bot is in another voice channel!")
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.hybrid_command(name="disconnect", description="Disconnects from the current voice channel")
    async def disconnect(self, ctx: commands.Context):

        if ctx.author.voice.channel == ctx.voice_client.channel:
            self.is_playing = False
            self.queue = []
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("You're not in the same channel as the bot!")

    async def _search_song(self, ctx: commands.Context, query: str):

        results = YoutubeSearch(query, max_results=5).to_dict()
        query_message = "> **Search Results**:\n"

        for index, result in enumerate(results):
            query_message += f"> {str(index + 1)}. {result['channel']} - {result['title']}\n"

        query_obj = await ctx.send(query_message, delete_after=60)
        reactions = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣")

        for reaction in reactions:
            await query_obj.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in reactions

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Too slow!", ephemeral=True)
        else:
            await self.play(ctx, query="https://youtube.com" + results[reactions.index(reaction.emoji)]["url_suffix"])

    @commands.hybrid_command(name="play", description="Plays a song, either via YouTube or direct video URL")
    async def play(self, ctx: commands.Context, *, query: str):

        if not query.startswith("https://"):
            await self._search_song(ctx, query)
            return

        await self.join(ctx)

        ydl_options = {'format': 'bestaudio'}
        voice_channel = ctx.voice_client

        with yt_dlp.YoutubeDL(ydl_options) as ydl:

            info = ydl.extract_info(query, download=False)

            song_info = {
                'title': info['title'],
                'uploader': info['uploader'],
                'thumbnail': info['thumbnail'],
                'page_url': info['webpage_url'],
                'duration': info['duration_string'],
                'author': ctx.message.author.name,
                'link': info['url']
            }

            embed = embed_song(song_info)
            self.queue.append(song_info)

            if not self.is_playing:
                source = await discord.FFmpegOpusAudio.from_probe(song_info['link'], **self.ffmpeg_options)
                self.is_playing = True

                await ctx.send(embed=embed, delete_after=60)
                voice_channel.play(source, after=lambda x=None: self._play_after(voice_channel, ctx.message.channel))

            else:
                await ctx.send(f"Adding **{song_info['title']}** to queue number **{len(self.queue)}**",
                               delete_after=10)

    @commands.hybrid_command(name="pause", description="Pauses the currently playing music")
    async def pause(self, ctx: commands.Context):

        if ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.pause()
            await ctx.send("Pausing music...")
        else:
            await ctx.send("You're not in the same channel as the bot!")

    @commands.hybrid_command(name="resume", description="Resumes the currently paused music")
    async def resume(self, ctx: commands.Context):

        if ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.resume()
            await ctx.send("Resuming music...")
        else:
            await ctx.send("You're not in the same channel as the bot!")

    @commands.hybrid_command(name="queue", description="Displays the current song queue")
    async def queue(self, ctx: commands.Context):

        message = "\n> **Queue:**"

        if len(self.queue) > 0:

            for i, item in enumerate(self.queue):
                message += f"\n> {i + 1}. {item['title']}"

                if i == 0:
                    message += " **[NOW PLAYING]**"

            await ctx.send(message, delete_after=10)

        else:
            await ctx.send("There are no songs in the queue!", delete_after=10)

    @commands.hybrid_command(name="skip", description="Skips the current song")
    async def skip(self, ctx: commands.Context):

        voice_client = ctx.voice_client

        if ctx.author.voice.channel == voice_client.channel:
            voice_client.stop()
            await ctx.send("Skipping current song", delete_after=5)

    @commands.hybrid_command(name="loop", description="Toggles looping for the current song")
    async def loop(self, ctx: commands.Context):

        if self.is_looping:
            self.is_looping = False
            await ctx.send("Loop: **OFF**")
        else:
            self.is_looping = True
            await ctx.send("Loop: **ON**")


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

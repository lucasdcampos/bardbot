import discord
from discord.ext import commands
from utils.downloader import Downloader
from utils.player import MusicPlayer
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    def get_player(self, ctx):
        if ctx.guild.id not in self.players:
            player = MusicPlayer(self.bot, ctx)
            self.players[ctx.guild.id] = player
            self.bot.loop.create_task(player.player_loop())
        return self.players[ctx.guild.id]

    @commands.command(name='play')
    async def play(self, ctx, *, query):
        if not ctx.author.voice:
            return await ctx.send("You need to be in a voice channel to use this command!")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        
        async with ctx.typing():
            try:
                path, title = await Downloader.download(query)
                player = self.get_player(ctx)
                player.queue.append({'path': path, 'title': title})
                await ctx.send(f"✅ Added to queue: **{title}**")
            except Exception as e:
                await ctx.send(f"An error occurred while processing the music: {e}")

    @commands.command(name='skip')
    async def skip(self, ctx):
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send("Nothing is playing right now!")
        
        ctx.voice_client.stop()
        await ctx.send("⏭️ Song skipped!")

    @commands.command(name='loop')
    async def loop(self, ctx, mode: str):
        mode = mode.lower()
        if mode not in ['off', 'song', 'queue']:
            return await ctx.send("Invalid mode! Use: `off`, `song` or `queue`.")
        
        player = self.get_player(ctx)
        player.loop_mode = mode
        await ctx.send(f"🔁 Loop mode changed to: **{mode}**")

    @commands.command(name='stop')
    async def stop(self, ctx):
        if ctx.guild.id in self.players:
            player = self.players[ctx.guild.id]
            player.stop()
            del self.players[ctx.guild.id]
        
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("🛑 Stopped and disconnected!")

async def setup(bot):
    await bot.add_cog(Music(bot))

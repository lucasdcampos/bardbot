import asyncio
import os
import discord

class MusicPlayer:
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        self.queue = []
        self.loop_mode = 'off' # 'off', 'song', 'queue'
        self.current = None
        self.voice_client = ctx.voice_client
        self.next_event = asyncio.Event()

    async def player_loop(self):
        while True:
            self.next_event.clear()

            if self.loop_mode == 'song' and self.current:
                # Keep the current song
                pass
            elif self.queue:
                if self.loop_mode == 'queue' and self.current:
                    self.queue.append(self.current)
                
                # Delete the previous song file if not looping the same song
                if self.current and self.loop_mode != 'song':
                    self.cleanup_file(self.current['path'])
                
                self.current = self.queue.pop(0)
            else:
                # If queue is empty and not in single song loop
                if self.current and self.loop_mode != 'song':
                    self.cleanup_file(self.current['path'])
                self.current = None
                await asyncio.sleep(1) # Wait for new songs
                if not self.queue:
                    continue

            if self.current:
                source = discord.FFmpegPCMAudio(self.current['path'])
                self.voice_client.play(source, after=lambda e: self.bot.loop.call_soon_threadsafe(self.next_event.set))
                await self.ctx.send(f"🎶 Now playing: **{self.current['title']}**")
                await self.next_event.wait()

    def cleanup_file(self, path):
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error deleting file {path}: {e}")

    def stop(self):
        self.queue.clear()
        if self.current:
            self.cleanup_file(self.current['path'])
            self.current = None
        if self.voice_client:
            self.voice_client.stop()

import yt_dlp
import os
import asyncio

# yt-dlp configuration
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class Downloader:
    @staticmethod
    async def get_info(query):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        
        if 'entries' in data:
            # Take first result if it's a search
            data = data['entries'][0]
            
        return {
            'title': data.get('title'),
            'url': data.get('webpage_url'),
            'id': data.get('id'),
            'ext': data.get('ext')
        }

    @staticmethod
    async def download(query):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=True))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        # Extension is now mp3 due to postprocessors
        file_path = f"music/{data['id']}.mp3"
        return file_path, data['title']
       file_path = f"music/{data['id']}.{data['ext']}"
        return file_path, data['title']

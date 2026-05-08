# Bard Bot

A private Discord bot for playing music from YouTube with your friends.

## Features

- `!!play <link or search>`: Joins your voice channel, downloads the audio, and adds it to the queue.
- `!!skip`: Skips the current track.
- `!!loop <off | song | queue>`: Toggles loop modes (off, repeat single song, or repeat entire queue).
- `!!stop`: Stops playback, clears the queue, and disconnects.
- **Automatic Cleanup**: Downloaded audio files are automatically deleted after playing or when the bot stops.

## Requirements

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/) installed and added to your system PATH.

## Setup

1. Clone this repository.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory (one was automatically generated) and add your Discord Token:
   ```env
   DISCORD_TOKEN=your_token_here
   ```
4. **Important**: Enable **Message Content Intent** in the [Discord Developer Portal](https://discord.com/developers/applications).
5. Run the bot:
   ```bash
   python main.py
   ```

## Tech Stack

- [discord.py](https://github.com/Rapptz/discord.py)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)

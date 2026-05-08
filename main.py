import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} is online!')
    
    # Cleanup music folder on startup
    if os.path.exists('music'):
        for file in os.listdir('music'):
            try:
                os.remove(os.path.join('music', file))
            except:
                pass
                
    try:
        await bot.load_extension('cogs.music')
        print("Music cog loaded successfully.")
    except Exception as e:
        print(f"Error loading music cog: {e}")

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

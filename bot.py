#python bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import common, add_song, get_songs, learning
import os
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(add_song.router)
    dp.include_router(get_songs.router)
    dp.include_router(learning.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
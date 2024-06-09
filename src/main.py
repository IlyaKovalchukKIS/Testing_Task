import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher

from src.bot import router
from src.pymongoAPI import create_db
from dotenv import load_dotenv

load_dotenv()


async def main_bot():
    bot = Bot(
        token=os.getenv("SECRET_KEY_TG"),
    )
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    create_db(
        host=os.getenv("HOST_DB"),
        port=int(os.getenv("PORT_DB")),
        db_name=os.getenv("NAME_DB"),
        collection=os.getenv("COLLECTION_DB"),
        filename_collection=os.getenv("FILENAME_DB"),
    )
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main_bot())

from aiogram import Bot,Dispatcher
from environs import Env
import asyncio
import logging

from handler import admin_router,user_router
import os

os.makedirs("images",exist_ok=True)

dp = Dispatcher()




async def main():
   
    TOKEN = os.getenv("TOKEN")
    bot = Bot(TOKEN)
    dp.include_router(admin_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except Exception as err:
        print(err)
        
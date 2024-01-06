import logging
import asyncio
from aiogram import Bot, Dispatcher
from config.bot_config import load_config
from handlers.user_handlers import router
from database.users import db_start
from FSMS.FSMS import storage


async def main():
    await db_start()

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    config = load_config()

    bot = Bot(token=config.token)
    dp = Dispatcher(storage=storage)

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
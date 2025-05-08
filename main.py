import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging
from app.user import user_router
from app.admin import admin_router
from database.Database import DataBase
from dotenv import load_dotenv
import os
# from core.log import Loger
from core.menu import set_commands
# # Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


# logger = Loger()
# logger.get_name_log(__name__)
# Загружаем переменные окружения
load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main():
    dp.include_routers(user_router, admin_router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    #  установка меню(список команд)
    await set_commands(bot)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    db = DataBase()
    await db.create_db()
    logger.info('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    db = DataBase()
    await db.close()
    logger.info('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Прерывание программы пользователем.")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    except RuntimeError as e:
        logger.error(f"Произошла ошибка: {e}")    
    
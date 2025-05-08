from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types
from database.Database import DataBase
from database.models import UserState
import logging
# from core.log import Loger
from core.dictionary import *
import app.keyboards as kb
# для работы с файлами
# import os
# from pathlib import Path
# import csv

# import re
# import locale
from datetime import datetime
from app.state import *
# Установка русской локали
# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)
# logger = Loger()
# logger.get_name_log(__name__)

admin_router = Router()


@admin_router.message(F.text.lower() == 'admin')
async def admin_command(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    logger.info(f'ID_TG:{telegram_id}|Команда старт ADMIN')
    await handle_admin_command(telegram_id, message, state)  # Передаем необходимые параметры


async def handle_admin_command(telegram_id: int, message: Message, state: FSMContext):
    await state.clear()
    db = DataBase()
    admin_tg = await db.check_admin(telegram_id)
    user_state = await db.get_state(telegram_id)

    # Удаляем старые сообщения, если есть
    await db.delete_messages(user_state)

    if admin_tg and admin_tg.id_tg == telegram_id:
        # await message.answer("Добро пожаловать!")
        sent_mess = await message.answer(text="Добро пожаловать!\nАдмин-меню:", reply_markup=await
        kb.inline_menu_admin())
        user_state.last_message_ids.append(sent_mess.message_id)
        await db.update_state(user_state)
    else:
        # await message.answer("У вас нет прав доступа.")
        return 
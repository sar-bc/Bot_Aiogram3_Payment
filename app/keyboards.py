from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from core.dictionary import *
import locale
from datetime import datetime, timedelta
from database.Database import DataBase
from collections import defaultdict

# Устанавливаем русскую локаль
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# ==================================================
async def inlite_start():
    kb = InlineKeyboardBuilder()
    kb.button(text="Купить подписку 1", callback_data=f'buy:1')
    kb.button(text="Купить подписку 2", callback_data=f'buy:2')
    return kb.adjust(1).as_markup()
# ===================================================
# Admin keyboars

async def inline_menu_admin():
    keyword = InlineKeyboardBuilder()
    keyword.row(
        InlineKeyboardButton(text=f"⬆️ Кнопка 1", callback_data='import_time_slots'),
        InlineKeyboardButton(text=f"⬇️ Кнопка 2", callback_data='export_time_slots')
    )
    
    keyword.row(InlineKeyboardButton(text=f"Отправить сообщение пользователям ✍️", callback_data='send_message'))
    return keyword.as_markup()

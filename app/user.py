from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice
from aiogram.filters import CommandStart, Command
from database.Database import DataBase
from database.models import UserState
# from core.log import Loger
from core.dictionary import *
import app.keyboards as kb
from dotenv import load_dotenv
import os
# import re
# import locale
import logging
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

user_router = Router()

######################
load_dotenv()
provider_token = os.getenv('PAYMENT_TOKEN')
currency = os.getenv('CURRENCY')
print(f'provider_token:{provider_token}')
#########################
@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f'ID_TG:{message.from_user.id}|Команда старт')
   
    db = DataBase()
    user_state = await db.get_state(message.from_user.id)
    await state.clear()
    await db.delete_messages(user_state)
   
    sent_mess =  await message.answer(welcom_text, reply_markup=await kb.inlite_start())
    user_state.last_message_ids.append(sent_mess.message_id)   
    await db.update_state(user_state)


#####################################################
########### ДЛЯ ОПЛАТЫ##############################
@user_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    logger.info(f'pre_checkout_query: {pre_checkout_query}')
    from main import bot
    # разные проверки
    # доступен ли товар 
    # Пример проверки на валидность платежа
    # if not is_payment_valid(pre_checkout_query):
    #     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Недостаточно средств.")
    #     return

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)





@user_router.callback_query(F.data.startswith('buy'))
async def callback_buy(callback: CallbackQuery, state: FSMContext):
    from main import bot
    logger.info(f"ID_TG:{callback.from_user.id}|=> callback_buy")
    db = DataBase()
    user_state = await db.get_state(callback.from_user.id)
    await db.delete_messages(user_state)
    await callback.answer()
    id = int(callback.data.split(':')[1])
    prices = []
    if id == 1:
        description = "Купить 1 раз"
        prices = [LabeledPrice(label="Оплата заказа № 1", amount=100 * 100)]
    if id == 2:
        description = "Купить 2 раза"
        prices = [LabeledPrice(label="Оплата заказа № 2", amount=200 * 100)]

    if prices:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f'Покупка {id}',
            description=description,
            payload=f'sub{id}',
            provider_token=provider_token,
            currency=currency,
            start_parameter='test',
            prices=prices
        )

@user_router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload_to_message = {
        'sub1': 'Подписка 1',
        'sub2': 'Подписка 2',
    }  
    response_message = payload_to_message.get(message.successful_payment.invoice_payload, 'Оплата успешно')
    await message.answer(response_message)  
from sqlalchemy import select, and_, delete, case, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import *
import os
import logging
from datetime import date
from datetime import datetime, timedelta
from core.dictionary import *
# from app.log import Loger

# # Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self):
        # For SQLITE
        self.connect = 'sqlite+aiosqlite:///db.sqlite3'
        self.async_engine = create_async_engine(url=self.connect, echo=False)
        self.Session = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)
        # For MySQL
        # self.db_host = os.getenv('DB_HOST')
        # self.db_user = os.getenv('DB_USER')
        # self.db_password = os.getenv('DB_PASSWORD')
        # self.db_name = os.getenv('DB_NAME')
        # self.connect = (f'mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}/'
        #                 f'{self.db_name}?charset=utf8mb4')
        # self.async_engine = create_async_engine(url=self.connect, echo=False)
        # self.Session = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)

    async def close(self):
        await self.async_engine.dispose()  # Закрытие соединения с базой данных

    async def create_db(self):
        async with self.async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

    async def get_state(self, id_tg: BigInteger):
            async with self.Session() as session:
                # Попытка получить состояние пользователя по user_id
                state = await session.scalar(select(UserState).where(UserState.user_id == id_tg))

                if state is None:
                    logger.info(f'Состояние не найдено для user_state_id: {id_tg}. Создание нового состояния.')
                    # Если состояния нет, создаем новое
                    state = UserState(user_id=id_tg)
                    session.add(state)
                    await session.commit()  # Сохраняем изменения
                    state = await session.scalar(select(UserState).where(UserState.user_id == id_tg))
                    logger.info(f'Создано состояние user_state:{state.user_id}')
                    return state
                else:
                    logger.info(f'Получено состояние для user_state_id: {id_tg}.')

                    return state

    async def delete_messages(self, state):
            if state.last_message_ids:
                from main import bot
                for lst in state.last_message_ids:
                    try:
                        await bot.delete_message(chat_id=state.user_id, message_id=lst)
                    except Exception as e:
                        logger.error(f"Ошибка при удалении сообщения: {e}")
                state.last_message_ids.clear()

    async def update_state(self, state: UserState):
            async with self.Session() as session:
                # Убедитесь, что объект связан с текущей сессией
                existing_state = await session.execute(select(UserState).where(UserState.user_id == state.user_id))
                current_state = existing_state.scalars().one_or_none()

                if current_state:
                    # Обновление атрибутов
                    current_state.last_message_ids = state.last_message_ids
                    
                    # Сохранение изменений
                    await session.commit()
                    return current_state  # Возвращаем обновленный объект
                else:
                    return None  # Состояние не найдено        

    async def log_to_db(self, level: str, message: str, logger_name: str):
        async with self.Session() as session:
            log_entry = Logs(
                timestamp=datetime.now(),  # Здесь можете использовать datetime.now().isoformat() для меток времени
                name=logger_name,
                level=level,
                message=message
            )
            session.add(log_entry)
            await session.commit()   

    async def check_admin(self, id_tg):
        async with self.Session() as session:
            result = await session.execute(select(AdminBot).where(AdminBot.id_tg == id_tg))
            return result.scalar()



from sqlalchemy import (ForeignKey, String, BigInteger,
                        TIMESTAMP, Column, func, Integer,
                        Text, CheckConstraint, Date, DateTime, Boolean, JSON, Time)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


####################################
class AdminBot(Base):
    __tablename__ = 'AdminBot'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_tg = Column(BigInteger, nullable=False)
    username = Column(String(100), nullable=True)

    def __repr__(self):
        return (f"<AdminBot(id={self.id}, id_tg={self.id_tg}, username={self.username})>")


####################################
class UserState(Base):
    __tablename__ = 'UserState'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    last_message_ids = Column(JSON, default=list)  # Поддержка JSON
    
    def __repr__(self):
        return (f"<UserState(id={self.id}, user_id={self.user_id}, "
                f"last_message_ids={self.last_message_ids})>")


####################################
class Logs(Base):
    __tablename__ = 'Logs'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    timestamp = Column(DateTime, nullable=False)  # Временная метка
    name = Column(Text, nullable=False)  # Имя логгера
    level = Column(Text, nullable=False)  # Уровень логирования
    message = Column(Text, nullable=False)  # Сообщение лога

    def __repr__(self):
        return (f"<Log(id={self.id}, timestamp='{self.timestamp}', "
                f"name='{self.name}', level='{self.level}', "
                f"message='{self.message}')>")


####################################

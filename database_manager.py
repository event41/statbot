# database_manager.py
# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, select

import config  # ← Убедись, что DATABASE_URL там есть

# Подключаемся к базе данных через SQLAlchemy
DATABASE_URL = config.DATABASE_URL or f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"

# Создаём движок
engine = create_async_engine(DATABASE_URL)

# Фабрика асинхронных сессий
AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# Модель таблицы "trades"
class TradeModel(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    bot_id = Column(String)
    exec_id = Column(String, unique=True)
    symbol = Column(String)
    side = Column(String)
    qty = Column(Float)
    price = Column(Float)
    profit = Column(Float)
    timestamp = Column(Integer)


# Инициализация БД
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы созданы или уже существуют")


# Сохранение сделки в БД
async def save_trade(session: AsyncSession, trade_data: dict):
    existing = await session.execute(
        select(TradeModel).where(TradeModel.exec_id == trade_data['exec_id'])
    )
    if existing.scalars().first():
        return  # Такая сделка уже есть

    new_trade = TradeModel(**trade_data)
    session.add(new_trade)
    await session.flush()
    print(f"📥 Сделка {trade_data['exec_id']} сохранена")
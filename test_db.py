# test_db.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import config

async def test_connection():
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
    )
    try:
        async with engine.begin() as conn:
            print("✅ Подключение к БД успешно!")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())

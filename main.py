# main.py
# -*- coding: utf-8 -*-

import asyncio
from bybit_api import get_recent_trades
from database_manager import init_db, save_trade
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


async def run_monitor(days=90):
    await init_db()

    bots = ["CB-1", "CB-2", "CB-3", "CB-4", "CB-5"]

    for bot_id in bots:
        print(f"\n🚀 Получаем сделки для {bot_id} за {days} дней...")
        trades = get_recent_trades(bot_id, days=days)
        print(f"📥 Найдено сделок для {bot_id}: {len(trades)}")

        async with AsyncSessionFactory() as session:
            async with session.begin():
                for trade_data in trades:
                    await save_trade(session, trade_data)
                await session.commit()


if __name__ == "__main__":
    # Для тестирования используем небольшой период
    asyncio.run(run_monitor(days=7))
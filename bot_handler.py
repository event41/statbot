# bot_handler.py
# -*- coding: utf-8 -*-

from telegram.ext import ApplicationBuilder, CommandHandler
from telegram_bot import stats_command, send_weekly_report, send_monthly_report, send_180day_report
import config

async def run_telegram_bot():
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("weekly", lambda u, c: send_weekly_report()))
    app.add_handler(CommandHandler("monthly", lambda u, c: send_monthly_report()))
    app.add_handler(CommandHandler("180days", lambda u, c: send_180day_report()))

    print("✅ Telegram-бот запущен. Ожидание команд...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()  # Держим бота в работе


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_telegram_bot())
# telegram_bot.py
# -*- coding: utf-8 -*-

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update, Bot
import asyncio
import stats
import config
from datetime import datetime


bot = Bot(token=config.TELEGRAM_BOT_TOKEN)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    bot_id = args[0] if len(args) > 0 else None
    period = args[1] if len(args) > 1 else "all"

    print(f"📥 Получена команда /stats от {update.effective_user.name}, аргументы: {args}")

    bots = ["CB-1", "CB-2", "CB-3", "CB-4", "CB-5"]
    result = ""

    if bot_id:
        stat = await stats.calculate_stats(bot_id, period)
        result += format_stat_block(stat)
    else:
        for b in bots:
            stat = await stats.calculate_stats(b, period)
            result += format_stat_block(stat)

    if update.message:
        await update.message.reply_text(result.strip(), parse_mode="HTML")


def send_weekly_report():
    asyncio.run(_send_report("week"))


def send_monthly_report():
    asyncio.run(_send_report("month"))


def send_180day_report():
    asyncio.run(_send_report("180days"))


async def _send_report(period):
    message = await get_stats_message(period=period)
    await bot.send_message(chat_id=config.TELEGRAM_CHANNEL, text=message, parse_mode="HTML")
    chat_info = await bot.get_chat(config.TELEGRAM_CHANNEL)
    msg_id = (await bot.get_messages(chat_info.id, limit=1))[0].id
    await bot.pin_chat_message(chat_info.id, msg_id)


async def get_stats_message(bot_id=None, period="all"):
    from stats import calculate_stats
    bots = ["CB-1", "CB-2", "CB-3", "CB-4", "CB-5"]
    result = ""

    if bot_id:
        stat = await calculate_stats(bot_id, period)
        result += format_stat_block(stat)
    else:
        for b in bots:
            stat = await calculate_stats(b, period)
            result += format_stat_block(stat)

    return result.strip()


def format_stat_block(stat):
    # Форматируем даты
    start_date = datetime.utcfromtimestamp(stat["first_trade_time"]).strftime("%Y-%m-%d") if stat["total_trades"] > 0 else "Нет данных"
    end_date = datetime.utcfromtimestamp(stat["last_trade_time"]).strftime("%Y-%m-%d") if stat["total_trades"] > 0 else datetime.utcfromtimestamp(int(time.time())).strftime("%Y-%m-%d")

    deposit = 5000
    profit = stat["total_profit"]

    if deposit != 0 and stat["total_trades"] > 0:
        profit_percent = round(profit / deposit * 100, 2)
        drawdown_percent = round(abs(stat["max_drawdown"]) / deposit * 100, 2)
    else:
        profit_percent = 0.0
        drawdown_percent = 0.0

    # Прибыль/убыток
    if profit > 0:
        profit_line = f"💰 <b>Общая прибыль: + ${profit} (↑ {profit_percent:.2f}%)</b>"
    elif profit < 0:
        profit_line = f"💸 <b>Общий убыток: - ${abs(profit)} (↓ -{abs(profit_percent):.2f}%)</b>"
    else:
        profit_line = "🟰 Общая прибыль: $0 (+0.00%)"

    return f"\n\n" + f"""\
🤖 <b>Бот: {stat["bot_id"]}</b>
📅 Период: с {start_date} по {end_date}

{profit_line}

🟢 Прибыльных сделок: {stat["win_rate"]}%
🔴 Убыточных сделок: {stat["loss_rate"]}%

📉 Максимальная просадка: ${stat["max_drawdown"]} (-{drawdown_percent:.2f}% от депозита)

📊 Всего сделок: {stat["total_trades"]}
🎯 Win/Loss Ratio: {stat["win_rate"]:.1f}% / {stat["loss_rate"]:.1f}%

{'=' * 30}
""".strip()
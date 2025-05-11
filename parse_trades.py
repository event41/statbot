def parse_trades(raw_trades, bot_id):
    parsed = []
    for trade in raw_trades:
        exec_time_ms = trade.get("execTime")  # Это уже в миллисекундах
        exec_id = trade.get("execId")
        symbol = trade.get("symbol")
        qty = float(trade.get("execQty", 0))
        price = float(trade.get("execPrice", 0))
        profit = float(trade.get("closedPnl", 0))  # ИСПОЛЬЗУЕМ closedPnl вместо execValue
        timestamp = int(exec_time_ms) // 1000 if exec_time_ms else int(time.time())

        parsed.append({
            "bot_id": bot_id,
            "exec_id": exec_id,
            "symbol": symbol,
            "side": trade.get("side"),
            "qty": qty,
            "price": price,
            "profit": profit,
            "timestamp": timestamp
        })
    return parsed
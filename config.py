# config.py
# -*- coding: utf-8 -*-

# 🤖 Настройки Telegram-бота
TELEGRAM_BOT_TOKEN = "7921337059:AAE5yilRWx0a9U3iCMMqnaM5eGxDBrT18Lg"  # Получи у @BotFather
TELEGRAM_CHANNEL = "@crashbotcopy"          # Укажи свой канал или None, если не нужен

# 📈 Настройки Bybit API
BOT_CREDENTIALS = {
    "CB-1": {
        "api_key": "A7xFU3Z9KrpZDWcMzq",
        "secret_key": "TdDCZSiBwO4Rsm4sMFBf2hZbEbIAIzBeMStZ"
    },
    "CB-2": {
        "api_key": "API_KEY_CB2",
        "secret_key": "SECRET_KEY_CB2"
    },
    "CB-3": {
        "api_key": "API_KEY_CB3",
        "secret_key": "SECRET_KEY_CB3"
    },
    "CB-4": {
        "api_key": "API_KEY_CB4",
        "secret_key": "SECRET_KEY_CB4"
    },
    "CB-5": {
        "api_key": "62LhBfHVYhMsg6bZOz",
        "secret_key": "vlqoaGKSgHkQyzctde1RU1TTgFIBGLG9FHWs"
    }
}

# 📊 Настройки базы данных (PostgreSQL + asyncpg)
DB_USER = "postgres"                     # Пользователь PostgreSQL
DB_PASSWORD = "1tnX2QXS6N8hClOr"           # Пароль пользователя
DB_HOST = "localhost"                    # Хост БД (IP или домен)
DB_PORT = 5432                          # Порт БД (по умолчанию 5432)
DB_NAME = "stata"                        # Имя твоей БД

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
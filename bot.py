from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
import os
from handlers import register_handlers  # Импортируем обработчики

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, загружается ли токен
if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN в .env!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрируем обработчики из handlers.py
register_handlers(dp)

if __name__ == "__main__":
    print("✅ Бот запускается...")
    executor.start_polling(dp, skip_updates=True)

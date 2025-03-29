from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv
import os
from handlers import register_handlers  # Импорт обработчиков

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, загружается ли токен
if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN в .env!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)  # В aiogram 3.x Dispatcher создается без параметров

# Регистрируем обработчики
register_handlers(dp)

async def main():
    print("✅ Бот запущен...")
    await dp.start_polling(bot)  # Теперь bot передается сюда

if __name__ == "__main__":
    asyncio.run(main())

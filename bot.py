import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import register_handlers  # Импортируем обработчики

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, загружается ли токен
if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в .env!")

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрируем обработчики
register_handlers(dp)

async def main():
    print("✅ Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

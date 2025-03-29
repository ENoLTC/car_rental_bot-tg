from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура выбора авто
car_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
car_keyboard.add(KeyboardButton("🚗 Эконом"), KeyboardButton("🚙 Комфорт"), KeyboardButton("🚘 Бизнес"))

# Клавиатура выбора времени аренды
time_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
time_keyboard.add(KeyboardButton("🕒 Весь день"), KeyboardButton("⏰ Почасовая аренда"))

# Клавиатура для выбора интервала времени в часах
hours_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for i in range(1, 24):  # Кнопки с интервалом от 1 до 23 часов
    hours_keyboard.add(KeyboardButton(f"⏰ {i} часов"))

# Клавиатура для согласия с правилами аренды
agree_disagree_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
agree_disagree_keyboard.add(KeyboardButton("✅ Согласен"), KeyboardButton("❌ Не согласен"))

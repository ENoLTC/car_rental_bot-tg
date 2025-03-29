from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для выбора автомобиля
car_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Эконом"), KeyboardButton(text="🚙 Комфорт")],
        [KeyboardButton(text="🚘 Бизнес")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора времени аренды
time_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🕒 Весь день")],
        [KeyboardButton(text="⏰ Почасовая аренда")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора количества часов
hours_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1 час"), KeyboardButton(text="2 часа"), KeyboardButton(text="3 часа")],
        [KeyboardButton(text="4 часа"), KeyboardButton(text="5 часов"), KeyboardButton(text="6 часов")]
    ],
    resize_keyboard=True
)

# Клавиатура для подтверждения согласия с правилами
agree_disagree_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Согласен")],
        [KeyboardButton(text="❌ Не согласен")]
    ],
    resize_keyboard=True
)

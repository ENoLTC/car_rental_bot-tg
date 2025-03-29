from aiogram import types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup
from config import ADMIN_CHAT_ID
from keyboards import car_keyboard, time_keyboard, hours_keyboard, agree_disagree_keyboard
import os
import re

# Хранилище данных пользователя
user_data = {}

# Шаг 1: Старт бота
async def start(message: types.Message):
    await message.answer("Привет! Выберите авто:", reply_markup=car_keyboard)

# Шаг 2: Выбор авто
async def choose_car(message: types.Message):
    user_data[message.from_user.id] = {"car": message.text}
    await message.answer("Выберите время аренды:", reply_markup=time_keyboard)

# Шаг 3: Выбор времени аренды (Весь день)
async def full_day(message: types.Message):
    user_data[message.from_user.id]["time"] = "Весь день"
    await send_rental_rules(message)

# Шаг 4: Выбор времени аренды (почасовая аренда)
async def hourly_rental(message: types.Message):
    await message.answer("Выберите количество часов аренды:", reply_markup=hours_keyboard)

async def choose_hours(message: types.Message):
  try:
    # Используем регулярку для извлечения первого числа из текста
    match = re.search(r"\d+", message.text)
    if match:
      hours = int(match.group())  # Преобразуем найденное число в int

      if 1 <= hours <= 23:
        user_data[message.from_user.id]["time"] = f"{hours} часов"
        await message.answer(f"Вы выбрали аренду на {hours} часов.", reply_markup=ReplyKeyboardRemove())
        await send_rental_rules(message)  # Переход на следующий шаг
      else:
        await message.answer("Пожалуйста, выберите от 1 до 23 часов.")
    else:
      await message.answer("❗ Не удалось определить количество часов. Выберите время кнопками.")
  except ValueError:
    await message.answer("❗ Ошибка при обработке данных. Выберите время кнопками.")

# Шаг 6: Отправка правил аренды и запрос согласия
async def send_rental_rules(message: types.Message):
    # Проверяем, не отправляли ли уже правила
    if "rules_sent" not in user_data.get(message.from_user.id, {}):
        user_data[message.from_user.id]["rules_sent"] = True
        await message.answer(
            "Пожалуйста, ознакомьтесь с правилами аренды: ...\n\nВы согласны с ними?",
            reply_markup=agree_disagree_keyboard
        )

# Шаг 7: Обработка нажатия на кнопки согласия
async def handle_agreement(message: types.Message):
    user_id = message.from_user.id

    if message.text == "✅ Согласен":
        user_data[user_id]["agreed"] = True
        await message.answer("Спасибо за согласие! Теперь загрузите фото ваших водительских прав.", reply_markup=ReplyKeyboardRemove())
    elif message.text == "❌ Не согласен":
        await message.answer("❗ Без согласия на правила аренды заявка не может быть оформлена.", reply_markup=ReplyKeyboardRemove())
        # Очищаем данные пользователя
        if user_id in user_data:
            del user_data[user_id]

# Шаг 8: Получение фото водительских прав
async def get_license_photo(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, согласился ли пользователь с правилами
    if user_data.get(user_id, {}).get("agreed"):
        if message.photo:
            user_data[user_id]["license_photo"] = message.photo[-1].file_id
            await submit_application(message)
        else:
            await message.answer("❗ Пожалуйста, загрузите фото ваших водительских прав.")
    else:
        await message.answer("❗ Пожалуйста, сначала согласитесь с правилами аренды.")

# Шаг 9: Отправка заявки в канал
async def submit_application(message: types.Message):
    user_id = message.from_user.id
    data = user_data.get(user_id, {})

    # Проверяем все необходимые данные
    if not all(key in data for key in ['car', 'time', 'license_photo']):
        await message.answer("❗ Не все данные заполнены. Пожалуйста, начните заново.", reply_markup=ReplyKeyboardRemove())
        if user_id in user_data:
            del user_data[user_id]
        return

    application_text = (
        f"Новая заявка на аренду авто!\n"
        f"👤 Пользователь: @{message.from_user.username}\n"
        f"🚘 Авто: {data['car']}\n"
        f"⏳ Время аренды: {data['time']}\n"
    )

    # Отправляем заявку в канал
    await message.bot.send_message(ADMIN_CHAT_ID, application_text)
    await message.bot.send_photo(ADMIN_CHAT_ID, photo=data["license_photo"])

    await message.answer("✅ Заявка отправлена! Ожидайте ответа.", reply_markup=ReplyKeyboardRemove())

    # Очищаем данные пользователя после отправки
    if user_id in user_data:
        del user_data[user_id]

# Регистрация обработчиков в диспетчере
def register_handlers(dp):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(choose_car, lambda message: message.text in ["🚗 Эконом", "🚙 Комфорт", "🚘 Бизнес"])
    dp.register_message_handler(full_day, lambda message: message.text == "🕒 Весь день")
    dp.register_message_handler(hourly_rental, lambda message: message.text == "⏰ Почасовая аренда")
    dp.register_message_handler(choose_hours, lambda message: message.text.endswith("час") or message.text.endswith("часов"))
    dp.register_message_handler(handle_agreement, lambda message: message.text in ["✅ Согласен", "❌ Не согласен"])
    dp.register_message_handler(get_license_photo, content_types=types.ContentType.PHOTO)
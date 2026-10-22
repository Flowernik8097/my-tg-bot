import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv('.env')

# Загружаем переменные из файла .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен не найден!")

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь: текст кнопки -> ответ бота
BUTTON_RESPONSES = {
    "Привет": "И тебе привет! Рад тебя видеть.",
    "Как дела?": "У ботов всё отлично, код компилируется без ошибок.",
    "Расскажи шутку": "Почему программисты путают Хэллоуин с Рождеством? Потому что 31 OCT = 25 DEC.",
    "Погода": "Внутри сервера всегда облачно, 22 градуса по Цельсию.",
    "Контакты": "Связаться с создателем: @ваш_никнейм_в_телеграме"
}


# Функция для генерации клавиатуры
def get_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text in BUTTON_RESPONSES.keys():
        builder.button(text=text, callback_data=text)
    builder.adjust(2)
    return builder.as_markup()


# Обработчик команды /start
@dp.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer("Выбери кнопку ниже:", reply_markup=get_main_keyboard())


# Обработчик нажатий на кнопки
@dp.callback_query()
async def handle_button_press(callback: types.CallbackQuery):
    button_text = callback.data

    if button_text in BUTTON_RESPONSES:
        response_text = BUTTON_RESPONSES[button_text]
        await callback.message.answer(response_text)
    else:
        await callback.message.answer("Извини, для этой кнопки пока нет ответа.")

    # Обязательно отвечаем на callback, чтобы убрать "крутилку" у пользователя
    await callback.answer()


# Точка входа. В aiogram 3.x нет executor!
async def main():
    # Пропускаем накопившиеся обновления, которые бот получил, пока был выключен
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
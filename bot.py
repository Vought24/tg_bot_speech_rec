import time
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import speech_recognition as sr

logging.basicConfig(level=logging.INFO)

TOKEN = ''

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
rec = sr.Recognizer()

# Создание inline-кнопки с обязательным callback_data
button_rec = InlineKeyboardBuilder()
button_rec.add(InlineKeyboardButton(text='Распознать голос', callback_data='recognize'))  # callback_data для привязки
inline_keyboard = button_rec.as_markup()

# Обработчик команды /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    
    # Отправляем приветственное сообщение с кнопкой
    await message.answer(f'Привет, {user_full_name}\nДавайте приступим к работе!', reply_markup=inline_keyboard)

# Обработчик команды /rec
@dp.message(Command('rec'))
async def recognize(message: types.Message):
    await message.answer("Скажите что-нибудь...")

    with sr.Microphone() as source:
        audio = rec.listen(source)

    try:
        text = rec.recognize_google(audio, language='ru-RU')
        await message.answer(f'Вы сказали:')
        await message.answer(text)
    except sr.UnknownValueError:
        await message.answer('Не удалось распознать речь...')
    except sr.RequestError as e:
        await message.answer(f'Ошибка распознавания: {e}')

# Обработчик нажатия кнопки с callback_data='recognize'
@dp.callback_query(lambda callback: callback.data == 'recognize')
async def handle_recognize_callback(callback: CallbackQuery):
    await callback.message.answer("Скажите что-нибудь...")

    with sr.Microphone() as source:
        audio = rec.listen(source)

    try:
        text = rec.recognize_google(audio, language='ru-RU')
        await callback.message.answer(f'Вы сказали: {text}')
    except sr.UnknownValueError:
        await callback.message.answer('Не удалось распознать речь...')
    except sr.RequestError as e:
        await callback.message.answer(f'Ошибка распознавания: {e}')
    
    # Обязательно ответьте на callback, чтобы Telegram убрал индикатор ожидания
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

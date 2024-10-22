from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEB_APP_URL = 'https://mygame.vercel.app'  # URL вашей игры

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Создаем кнопку с веб-приложением
    web_app = WebAppInfo(url=WEB_APP_URL)
    button = InlineKeyboardButton("Играть в 'Четыре в ряд'", web_app=web_app)
    keyboard = InlineKeyboardMarkup().add(button)

    await message.answer("Нажмите на кнопку ниже, чтобы начать игру:", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
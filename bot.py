from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, Update
from aiohttp import web
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEB_APP_URL = 'https://fourinarow-production.up.railway.app'  # URL вашей игры

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик вебхука
async def handle_webhook(request):
    try:
        # Получаем JSON из запроса и преобразуем в объект Update
        data = await request.json()
        update = Update(**data)  # Преобразуем JSON в Update

        # Передаём обновление диспетчеру
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        print(f"Ошибка при обработке вебхука: {e}")
        return web.Response(status=500)

# Обработчик команды /start
@dp.message(commands=['start'])
async def start_handler(message: types.Message):
    web_app = WebAppInfo(url=WEB_APP_URL)
    button = InlineKeyboardButton("Играть в 'Четыре в ряд'", web_app=web_app)
    keyboard = InlineKeyboardMarkup().add(button)
    await message.answer("Нажмите на кнопку ниже, чтобы начать игру:", reply_markup=keyboard)

# Настройка веб-приложения
app = web.Application()
app.router.add_post("/webhook", handle_webhook)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
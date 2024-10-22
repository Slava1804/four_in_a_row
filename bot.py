import os
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.token import TokenValidationError
from aiohttp import web
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получаем токен и проверяем его корректность
try:
    API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token=API_TOKEN)
except TokenValidationError:
    print("Неверный токен. Проверьте TELEGRAM_BOT_TOKEN в .env")

# URL вашего веб-приложения
WEB_APP_URL = "https://fourinarow-production.up.railway.app"  # Ваш новый домен

# Инициализация диспетчера и роутера
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Маршрут для команды /start
@router.message(lambda message: message.text == "/start")
async def start_handler(message: Message):
    web_app = WebAppInfo(url=WEB_APP_URL)
    button = InlineKeyboardButton(text="Играть в 'Четыре в ряд'", web_app=web_app)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("Нажмите на кнопку ниже, чтобы начать игру:", reply_markup=keyboard)

# Вебхуки
async def on_startup(app):
    webhook_url = f"{WEB_APP_URL}/webhook"
    await bot.set_webhook(webhook_url)

async def on_shutdown(app):
    await bot.session.close()

# Настройка веб-сервера
async def main():
    app = web.Application()
    app.on_startup.append(on_startup)  # Регистрация функции старта
    app.on_cleanup.append(on_shutdown)  # Регистрация функции завершения
    return app

if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
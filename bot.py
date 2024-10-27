from aiohttp import web
from aiogram import Bot, Dispatcher, types, Router
from aiogram.webhook.aiohttp_server import setup_application
from dotenv import load_dotenv
import os

# Загружаем токен из .env
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Обработчик для команды /start
# @router.message(commands=["start"])
# async def start_handler(message: types.Message):
#     await message.answer("Привет! Бот работает.")

# Включаем маршруты в диспетчер
dp.include_router(router)

# Обработчик для вебхука
async def handle_webhook(request):
    update = await request.json()  # Получаем обновление от Telegram
    await dp.feed_update(bot, update)  # Передаём обновление диспетчеру
    return web.Response(text="OK")  # Ответ Telegram'у

# Основная функция для настройки и запуска приложения
async def main():
    app = web.Application()  # Создаём приложение Aiohttp
    app.router.add_post("/webhook", handle_webhook)  # Регистрируем маршрут для вебхука
    setup_application(app, dp, bot=bot)  # Настраиваем приложение с диспетчером
    return app  # Возвращаем готовое приложение

# Запуск приложения на указанном хосте и порту
if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
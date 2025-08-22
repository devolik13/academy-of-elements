import os
import asyncio
from contextlib import asynccontextmanager

# --- Импорты для FastAPI ---
from fastapi import FastAPI
import uvicorn

# --- Импорты для aiogram ---
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.types import Update

# --- Импорты из вашего проекта ---
from dotenv import load_dotenv
from app import create_app

# --- Загрузка переменных окружения ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# --- Инициализация бота и диспетчера ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Webhook настройки ---
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://your-app.onrender.com{WEBHOOK_PATH}"  # ЗАМЕНИТЕ на ваш URL

async def set_webhook():
    """Установка webhook"""
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook установлен: {WEBHOOK_URL}")

async def delete_webhook():
    """Удаление webhook"""
    await bot.delete_webhook()
    print("✅ Webhook удален")

# --- Создание приложения FastAPI ---
app = create_app(dp, bot)

# --- Роут для обработки webhook ---
@app.post(WEBHOOK_PATH)
async def handle_webhook(update: dict):
    """Обработчик webhook от Telegram"""
    try:
        telegram_update = Update(**update)
        await dp.feed_update(bot=bot, update=telegram_update)
        return {"status": "ok"}
    except Exception as e:
        print(f"❌ Ошибка обработки webhook: {e}")
        return {"status": "error", "message": str(e)}

# --- Обработчики событий FastAPI ---
@app.on_event("startup")
async def on_startup():
    """Выполняется при запуске приложения"""
    await set_webhook()

@app.on_event("shutdown")
async def on_shutdown():
    """Выполняется при остановке приложения"""
    await delete_webhook()

# --- ОСНОВНОЙ ЦИКЛ ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Запуск приложения на порту {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)import os
from contextlib import asynccontextmanager

# --- Импорты для FastAPI ---
from fastapi import FastAPI
import uvicorn

# --- Импорты для aiogram ---
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

# --- Импорты из вашего проекта ---
from dotenv import load_dotenv
from app import create_app

# --- Загрузка переменных окружения ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# --- Инициализация бота и диспетчера ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Webhook настройки ---
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://https://academy-of-elements-1.onrender.com{WEBHOOK_PATH}"  # ЗАМЕНИТЕ на ваш URL

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

# --- Создание приложения FastAPI ---
app = create_app(dp, bot)

# --- Регистрация webhook ---
@app.on_event("startup")
async def startup_event():
    await on_startup(bot)

@app.on_event("shutdown")
async def shutdown_event():
    await on_shutdown(bot)

# Регистрируем обработчик webhook
webhook_requests_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)
webhook_requests_handler.register(app, path=WEBHOOK_PATH)

# --- ОСНОВНОЙ ЦИКЛ ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Запуск приложения на порту {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

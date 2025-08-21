# main.py
import asyncio
import os
from contextlib import asynccontextmanager

# --- Импорты для FastAPI ---
from fastapi import FastAPI
import uvicorn

# --- Импорты для aiogram ---
from aiogram import Bot, Dispatcher

# --- Импорты из вашего проекта ---
from dotenv import load_dotenv
from app import create_app # Импортируем функцию создания приложения

# --- Загрузка переменных окружения ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# --- Инициализация бота и диспетчера ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Создание приложения FastAPI ---
# Всё необходимое теперь внутри create_app
app = create_app(dp, bot)

# --- ОСНОВНОЙ ЦИКЛ ---
if __name__ == "__main__":
    print("🚀 Запуск приложения...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

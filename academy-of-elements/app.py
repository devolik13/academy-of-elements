# app.py
import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Dispatcher, Bot
from aiogram.filters import Command

# Импорты обработчиков
from handlers.user_handlers import cmd_start, select_faction
from handlers.building_handlers import cmd_buildings, cmd_build, cmd_upgrade
from handlers.wizard_handlers import cmd_profile, cmd_wizards, cmd_spells, cmd_research, cmd_cancel_research, cmd_hire_wizard
from handlers.city_handler import open_city
from api.building_api import api_build

def create_app(dp: Dispatcher, bot: Bot) -> FastAPI:
    """Создает и конфигурирует FastAPI приложение."""

    # --- Настройка FastAPI ---
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Код до запуска сервера
        print("🚀 FastAPI сервер готов.")
        # Запускаем polling бота в фоновой задаче
        task = asyncio.create_task(dp.start_polling(bot))
        print("🤖 Telegram бот запущен.")
        yield
        # Код после остановки сервера
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        print("🛑 Telegram бот остановлен.")

    app = FastAPI(lifespan=lifespan)

    # --- Регистрация обработчиков команд ---
    # User handlers
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(select_faction, Command("fire", "water", "wind", "earth"))

    # Building handlers
    dp.message.register(cmd_buildings, Command("buildings"))
    dp.message.register(cmd_build, Command("build"))
    dp.message.register(cmd_upgrade, Command("upgrade"))

    # Wizard handlers
    dp.message.register(cmd_profile, Command("profile"))
    dp.message.register(cmd_wizards, Command("wizards"))
    dp.message.register(cmd_spells, Command("spells"))
    dp.message.register(cmd_research, Command("research"))
    dp.message.register(cmd_cancel_research, Command("cancel_research"))
    dp.message.register(cmd_hire_wizard, Command("hire_wizard"))

    # City handler
    dp.message.register(open_city, Command("city"))

    # --- Настройка CORS ---
    # Исправлены origins (убраны лишние пробелы)
    origins = [
        "https://academy-of-elements.vercel.app",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- FastAPI Endpoints ---
    # Роуты для веб-интерфейса
    @app.get("/")
    async def read_index():
        return FileResponse("web/index.html")

    @app.get("/city")
    async def read_city():
        return FileResponse("web/index.html")

    # API endpoints
    @app.get("/api/health")
    async def health_check():
        return {"status": "ok", "message": "FastAPI сервер Academy of Elements работает!"}

    @app.get("/api/test")
    async def test_api():
        return {"message": "FastAPI API работает!"}

    # Подключение API endpoint для постройки
    app.post("/api/build")(api_build)

    # --- Настройка статических файлов ---
    # Проверяем, существует ли папка web
    web_dir = "web"
    if os.path.isdir(web_dir):
        # Монтируем папку web для раздачи статических файлов
        app.mount("/static", StaticFiles(directory=web_dir), name="static")
        # Для изображений зданий
        app.mount("/images", StaticFiles(directory=os.path.join(web_dir, "images")), name="images")
        # Для изображений заклинаний (когда появятся)
        # app.mount("/spells", StaticFiles(directory=os.path.join(web_dir, "spells")), name="spells")
        print(f"📁 Статические файлы подключены из папки '{web_dir}'")
    else:
        print(f"⚠️ Папка '{web_dir}' не найдена. Статические файлы не будут обслуживаться.")

    return app
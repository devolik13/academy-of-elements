# main.py (для Yandex Cloud Function)
import os
import json
import asyncio
import logging
from typing import Dict, Any

# --- Импорты для aiogram ---
from aiogram import Bot, Dispatcher
from aiogram.types import Update

# --- Импорты из вашего проекта ---
from dotenv import load_dotenv
from app import create_app  # Этот импорт может понадобиться для регистрации обработчиков

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Загрузка переменных окружения ---
# В YC Function переменные окружения устанавливаются через консоль/terraform
load_dotenv()

# Глобальные переменные для бота и диспетчера
bot = None
dp = None

async def initialize_bot():
    """Асинхронная инициализация бота и диспетчера"""
    global bot, dp
    
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    # --- Инициализация бота и диспетчера ---
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # --- Регистрация обработчиков команд ---
    # Нужно импортировать и зарегистрировать все обработчики
    try:
        from handlers.user_handlers import cmd_start, select_faction
        from handlers.building_handlers import cmd_buildings, cmd_build, cmd_upgrade
        from handlers.wizard_handlers import cmd_profile, cmd_wizards, cmd_spells, cmd_research, cmd_cancel_research, cmd_hire_wizard
        from handlers.city_handler import open_city
        
        from aiogram.filters import Command
        
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
        
        logger.info("✅ Обработчики зарегистрированы")
    except Exception as e:
        logger.error(f"❌ Ошибка регистрации обработчиков: {e}")
        raise

# Флаг для отслеживания инициализации
initialized = False

async def init_once():
    """Инициализация только один раз"""
    global initialized
    if not initialized:
        await initialize_bot()
        initialized = True

def is_health_check(event: Dict[str, Any]) -> bool:
    """Проверка, является ли запрос health check'ом от Yandex Cloud"""
    # YC может периодически делать health check запросы
    # Обычно это HEAD или GET запросы без тела
    if 'body' not in event or not event['body']:
        return True
    try:
        body = json.loads(event['body'])
        # Простая проверка на пустое тело или спеотивные признаки
        return not body or 'update_id' not in body
    except:
        return True

async def process_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Обработка события от Telegram"""
    try:
        # Парсим тело запроса
        body = event.get('body', '{}')
        if not body:
            logger.info("Получен пустой запрос (возможно health check)")
            return {
                'statusCode': 200,
                'body': 'OK - Health Check',
                'headers': {'Content-Type': 'text/plain'}
            }
            
        update_dict = json.loads(body)
        logger.info(f"Получен Update: {update_dict.get('update_id', 'unknown')}")
        
        # Создаем объект Update
        telegram_update = Update(**update_dict)
        
        # Обрабатываем обновление
        await dp.feed_update(bot, telegram_update)
        
        return {
            'statusCode': 200,
            'body': 'OK',
            'headers': {'Content-Type': 'text/plain'}
        }
    except json.JSONDecodeError as e:
        logger.error(f"❌ Ошибка парсинга JSON: {e}")
        return {
            'statusCode': 400,
            'body': 'Bad Request - Invalid JSON',
            'headers': {'Content-Type': 'text/plain'}
        }
    except Exception as e:
        logger.error(f"❌ Ошибка обработки webhook: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': 'Internal Server Error',
            'headers': {'Content-Type': 'text/plain'}
        }

async def handler(event, context):
    """
    Точка входа для Yandex Cloud Function.
    
    Args:
        event (Dict): Событие от YC Function (содержит HTTP запрос)
        context: Контекст выполнения функции
        
    Returns:
        Dict: HTTP ответ
    """
    try:
        # Инициализация бота при первом вызове
        await init_once()
        
        # Обработка события
        response = await process_event(event)
        return response
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка в handler: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': 'Internal Server Error',
            'headers': {'Content-Type': 'text/plain'}
        }

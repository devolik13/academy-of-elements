# handlers/building_handlers.py
from aiogram import types
from database import UserDatabase
from building_manager import BuildingManager
from buildings_config import BUILDINGS_DATA

async def cmd_buildings(message: types.Message):
    """Показать информацию о зданиях игрока"""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        buildings = user_data.get("buildings", {})
        construction = user_data.get("construction", {})
        
        if not buildings:
            await message.answer("🏗️ У тебя пока нет построенных зданий.")
            return

        response_text = "🏗️ **Твои здания:**\n\n"
        
        for building_id, building_info in buildings.items():
            # Получаем данные о здании из конфигурации
            building_data = BUILDINGS_DATA.get(building_id, {})
            building_name = building_data.get("name", building_id)
            building_emoji = building_data.get("emoji", "🏛️")
            building_level = building_info.get("level", 1)
            
            response_text += f"{building_emoji} **{building_name}** (уровень {building_level})\n"
            
            # Добавляем описание эффектов, если они есть
            effects = building_data.get("effects", {})
            if effects:
                # Здесь можно добавить более подробное описание эффектов
                # в зависимости от типа здания и его уровня
                pass
                 
            response_text += "\n"

        # Добавляем информацию об активной постройке
        if construction.get("active", False):
            building_id = construction.get("building_id")
            target_level = construction.get("target_level")
            time_left = construction.get("time_left", 0)
            construction_type = construction.get("type", "build")
            
            # Получаем название здания
            building_name = "Неизвестное здание"
            building_data = BUILDINGS_DATA.get(building_id)
            if building_data:
                building_name = building_data.get("name", building_id)
                building_emoji = building_data.get("emoji", "🏛️")
            
            type_text = "постройка" if construction_type == "build" else "улучшение"
            target_text = f"до уровня {target_level}" if construction_type == "upgrade" else ""
            
            response_text += f"⏳ **Активная постройка:**\n"
            response_text += f"{building_emoji} {building_name} ({type_text} {target_text}, {time_left} дней осталось)\n"
        else:
            response_text += "⏳ Нет активных построек\n"

        await message.answer(response_text, parse_mode="Markdown")

    except Exception as e:
        print(f"❌ Ошибка в /buildings: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при получении информации о зданиях.")

async def cmd_build(message: types.Message):
    """Начать постройку здания. Используется из Telegram."""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        args = message.text.split()[1:]
        if not args:
            await message.answer(
                "❌ Укажите ID здания для постройки и, опционально, индекс ячейки.\n"
                "Пример: `/build aom_generator 10` (построить в ячейке 10)\n"
                "Если ячейка не указана, будет выбрана первая свободная.",
                parse_mode="Markdown"
            )
            return

        building_id = args[0]
        cell_index = None
        if len(args) > 1:
             try:
                 cell_index = int(args[1])
             except ValueError:
                 await message.answer("❌ Индекс ячейки должен быть числом.")
                 return

        building_data = BUILDINGS_DATA.get(building_id)
        if not building_data:
            await message.answer(f"❌ Здание с ID '{building_id}' не найдено.")
            return

        if not building_data.get("can_build", False):
            await message.answer(f"❌ Здание '{building_data['name']}' нельзя построить.")
            return

        # Если cell_index не задан, можно попробовать найти первую пустую ячейку
        # Это простая реализация, возможно, потребуется улучшение
        if cell_index is None:
            buildings_grid = user_data.get("buildings_grid", [None] * 9)
            try:
                cell_index = buildings_grid.index(None) # Найти первый None
            except ValueError:
                await message.answer("❌ Нет свободных ячеек для постройки.")
                return

        # Начинаем постройку через BuildingManager
        success, msg = await BuildingManager.start_construction(user_id, building_id, cell_index)
        await message.answer(msg)

    except Exception as e:
        print(f"❌ Ошибка в /build: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при начале постройки.")

async def cmd_upgrade(message: types.Message):
    """Начать улучшение здания"""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        # Разбираем аргументы команды
        args = message.text.split()[1:]  # Убираем "/upgrade"
        if len(args) < 2:
            await message.answer(
                "❌ Укажите ID здания и целевой уровень.\n"
                "Пример: `/upgrade aom_generator 2`",
                parse_mode="Markdown"
            )
            return

        building_id = args[0]
        try:
            target_level = int(args[1])
        except ValueError:
            await message.answer("❌ Уровень должен быть числом.")
            return

        # Проверяем, существует ли такое здание
        building_data = BUILDINGS_DATA.get(building_id)
        if not building_data:
            await message.answer(f"❌ Здание с ID '{building_id}' не найдено.")
            return

        # Начинаем улучшение через BuildingManager
        success, msg = await BuildingManager.start_upgrade(user_id, building_id, target_level)
        await message.answer(msg)

    except Exception as e:
        print(f"❌ Ошибка в /upgrade: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при начале улучшения.")
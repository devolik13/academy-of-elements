# building_manager.py
"""Менеджер зданий для Academy of Elements."""

from buildings_config import get_building_data, get_building_time, get_max_level
from database import UserDatabase
import asyncio

class BuildingManager:
    """Класс для управления зданиями игрока."""
    
    @staticmethod
    async def can_build(user_id, building_id):
        """
        Проверить, может ли игрок построить здание.
        
        Args:
            user_id (str): ID пользователя.
            building_id (str): ID здания.
            
        Returns:
            tuple: (bool, str) - (Можно ли строить, Сообщение об ошибке/успехе)
        """
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            return False, "Пользователь не найден."
            
        building_data = get_building_data(building_id)
        if not building_data:
            return False, "Здание не найдено."
            
        # Проверка, можно ли строить это здание
        if not building_data["can_build"]:
            return False, f"Здание '{building_data['name']}' нельзя построить."
            
        # Проверка, является ли здание уникальным и уже построено
        if building_data["is_unique"]:
            # Проверяем, есть ли уже активная постройка/улучшение
            construction = user_data.get("construction", {})
            if construction.get("active", False) and construction.get("building_id") == building_id:
                return False, f"Уже идет работа над '{building_data['name']}'."
                
            # Проверяем, построено ли здание (для уникальных)
            # Это упрощенная проверка, в реальной реализации может быть сложнее
            # Например, можно хранить информацию о построенных уникальных зданиях отдельно
            
        # Проверка, есть ли активная постройка
        construction = user_data.get("construction", {})
        if construction.get("active", False):
            return False, "У вас уже идет одна постройка. Дождитесь её завершения."
            
        return True, "Можно строить."

    @staticmethod
    async def start_construction(user_id, building_id, cell_index=None):
        """
        Начать постройку здания.

        Args:
            user_id (str): ID пользователя.
            building_id (str): ID здания.
            cell_index (int, optional): Индекс ячейки в сетке (для визуального расположения).

        Returns:
            tuple: (bool, str) - (Успешно ли начата постройка, Сообщение)
        """
        can_build, message = await BuildingManager.can_build(user_id, building_id)
        if not can_build:
            return False, message

        building_data = get_building_data(building_id)
        build_time = get_building_time(building_id)

        # Начинаем постройку (или сразу завершаем, если время 0)
        construction_data = {
            "active": True, # Даже для мгновенной постройки сначала активируем
            "building_id": building_id,
            "target_level": 1, # Для новой постройки целевой уровень 1
            "time_left": build_time, # Это будет 0
            "cell_index": cell_index,
            "type": "build" # Тип операции: build или upgrade
        }

        # Если время 0, сразу завершаем постройку
        if build_time <= 0:
             success = await UserDatabase.finish_construction(user_id, building_id, 1, cell_index)
             if success:
                 # Начисляем кристаллы за мгновенную постройку (пример, можно убрать или изменить)
                 # user_data = await UserDatabase.get_user(user_id)
                 # if user_data:
                 #     new_crystals = user_data.get('crystals', 0) + 10
                 #     await UserDatabase.update_user(user_id, {"crystals": new_crystals})
                 return True, f"✅ '{building_data['name']}' построен мгновенно!"
             else:
                 return False, "Ошибка при мгновенной постройке."

        success = await UserDatabase.start_construction(user_id, construction_data)
        if success:
            return True, f"Начата постройка '{building_data['name']}'. Время: {build_time} секунд."
        else:
            return False, "Ошибка при начале постройки."

    @staticmethod
    async def can_upgrade(user_id, building_id, target_level):
        """
        Проверить, может ли игрок улучшить здание.
        
        Args:
            user_id (str): ID пользователя.
            building_id (str): ID здания.
            target_level (int): Целевой уровень для улучшения.
            
        Returns:
            tuple: (bool, str) - (Можно ли улучшать, Сообщение об ошибке/успехе)
        """
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            return False, "Пользователь не найден."
            
        building_data = get_building_data(building_id)
        if not building_data:
            return False, "Здание не найдено."
            
        # Проверка максимального уровня
        max_level = get_max_level(building_id)
        if target_level > max_level:
            return False, f"Максимальный уровень для '{building_data['name']}': {max_level}."
            
        # Проверка текущего уровня (в упрощенном виде)
        # В реальной реализации нужно хранить текущий уровень каждого здания
        # Пока предположим, что все здания начинаются с уровня 0 или 1
        
        # Проверка, есть ли активная постройка/улучшение
        construction = user_data.get("construction", {})
        if construction.get("active", False):
            return False, "У вас уже идет одна постройка/улучшение. Дождитесь её завершения."
            
        return True, "Можно улучшать."

    @staticmethod
    async def start_upgrade(user_id, building_id, target_level):
        """
        Начать улучшение здания.

        Args:
            user_id (str): ID пользователя.
            building_id (str): ID здания.
            target_level (int): Целевой уровень для улучшения.

        Returns:
            tuple: (bool, str) - (Успешно ли начато улучшение, Сообщение)
        """
        can_upgrade, message = await BuildingManager.can_upgrade(user_id, building_id, target_level)
        if not can_upgrade:
            return False, message

        building_data = get_building_data(building_id)
        upgrade_time = get_building_time(building_id, target_level)

        # Начинаем улучшение (или сразу завершаем, если время 0)
        construction_data = {
            "active": True,
            "building_id": building_id,
            "target_level": target_level,
            "time_left": upgrade_time, # Это будет 0
            "type": "upgrade" # Тип операции: build или upgrade
        }

        # Если время 0, сразу завершаем улучшение
        if upgrade_time <= 0:
             success = await UserDatabase.finish_construction(user_id, building_id, target_level)
             if success:
                 return True, f"✅ '{building_data['name']}' улучшен до уровня {target_level} мгновенно!"
             else:
                 return False, "Ошибка при мгновенном улучшении."

        success = await UserDatabase.start_construction(user_id, construction_data)
        if success:
            return True, f"Начато улучшение '{building_data['name']}' до уровня {target_level}. Время: {upgrade_time} секунд."
        else:
            return False, "Ошибка при начале улучшения."

    @staticmethod
    async def get_user_buildings_info(user_id):
        """
        Получить информацию о зданиях пользователя.
        
        Args:
            user_id (str): ID пользователя.
            
        Returns:
            dict: Информация о зданиях.
        """
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            return {}
            
        # Здесь можно собрать информацию о построенных зданиях,
        # их текущих уровнях, активных постройках и т.д.
        # Пока возвращаем базовую информацию
        return {
            "buildings": user_data.get("buildings", []),
            "construction": user_data.get("construction", {}),
            # В будущем можно добавить информацию о текущих уровнях зданий
        }
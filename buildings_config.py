# buildings_config.py
"""Конфигурация зданий для Academy of Elements."""

# Описание типов зданий и их параметров
BUILDINGS_DATA = {
    "library": {
        "id": "library",
        "name": "Библиотека",
        "description": "Центр исследований заклинаний.",
        "emoji": "📚",
        "is_unique": True,
        "is_starting": True,
        "can_build": False,
        "max_level": 1,
        "costs": {
            "build_time": 0, # Не строится отдельно
            "upgrade_times": [] # Нет улучшений
        },
        "effects": {
            "function": "research_center"
        }
    },
    "wizard_tower": {
        "id": "wizard_tower",
        "name": "Башня магов",
        "description": "Усиливает магов и позволяет нанимать новых.",
        "emoji": "🧙‍♂️",
        "is_unique": True,
        "is_starting": True,
        "can_build": False, # Уже есть, не строится
        "max_level": 10,
        "costs": {
            "build_time": 0, # Не строится отдельно
            # Время улучшений: Уровень N - 2^(N-1) дней
            "upgrade_times": [2**(i-1) for i in range(1, 11)] # [1, 2, 4, 8, ..., 512]
        },
        "effects": {
            "health_bonus_per_level": 10, # +10% к здоровью за уровень
            "spell_power_levels": {3: 10, 6: 20, 9: 30}, # +10% на 3, +20% на 6, +30% на 9
            "level_10_bonus": "duplicate_spell_slot" # Возможность добавлять заклинание еще раз
        }
    },
    "blessing_tower": {
        "id": "blessing_tower",
        "name": "Башня благословений",
        "description": "Открывает мощные временные благословения для магов.",
        "emoji": "🛐",
        "is_unique": True,
        "is_starting": False,
        "can_build": True,
        "max_level": 5,
        "costs": {
            "build_time": 15, # Примерное время постройки (можно изменить)
            # Время улучшений: Уровень N - 10 * 2^(N-1) дней
            "upgrade_times": [10 * (2**(i-1)) for i in range(1, 6)] # [10, 20, 40, 80, 160]
        },
        "effects": {
            "blessings_unlocked": list(range(1, 6)) # Открывает 1-е по 5-е благословение
        }
    },
    "aom_generator": {
        "id": "aom_generator",
        "name": "Генератор АОМ",
        "description": "Производит кристаллы AOM - основную валюту.",
        "emoji": "💎",
        "is_unique": True,
        "is_starting": False,
        "can_build": True,
        "max_level": 20,
        "costs": {
            "build_time": 1, # Время постройки
            # Улучшения: каждый уровень на 20% дольше предыдущего
            # Уровень 2: 1 * 1.2 = 1.2 дня, Уровень 3: 1.2 * 1.2 = 1.44 дня и т.д.
            "upgrade_times": [] # Будет рассчитано по формуле
        },
        "effects": {
            "aom_base_production": 100, # Базовая добыча 100 AOM/день
            "aom_production_multiplier": 1.2 # +20% за уровень
        }
    },
    "pvp_arena": {
        "id": "pvp_arena",
        "name": "PvP Арена",
        "description": "Проведение боев 1 на 1 по принципу autochess с рейтингом.",
        "emoji": "⚔️",
        "is_unique": True,
        "is_starting": False,
        "can_build": True,
        "max_level": 1,
        "costs": {
            "build_time": 7, # Примерное время постройки (нужно определить)
            "upgrade_times": [] # Нет улучшений
        },
        "effects": {
            "function": "pvp_battles_1v1",
            "rating_system": True,
            "battle_logs": True
        }
    },
    "defense_tower": {
        "id": "defense_tower",
        "name": "Башня защиты",
        "description": "Защищает город, используя изученные заклинания.",
        "emoji": "🛡️",
        "is_unique": True,
        "is_starting": False,
        "can_build": True,
        "max_level": 5,
        "costs": {
            "build_time": 12, # Примерное время постройки (нужно определить)
            # Время улучшений: Уровень N - 10 * 2^(N-1) дней
            "upgrade_times": [10 * (2**(i-1)) for i in range(1, 6)] # [10, 20, 40, 80, 160]
        },
        "effects": {
            "spells_used": "equal_to_level" # Количество заклинаний = уровень башни
        }
    },
    "arcane_lab": {
        "id": "arcane_lab",
        "name": "Арканская лаборатория",
        "description": "Ускоряет процесс исследования заклинаний.",
        "emoji": "⚗️",
        "is_unique": True,
        "is_starting": False,
        "can_build": True,
        "max_level": 15,
        "costs": {
            "build_time": 3, # Примерное время постройки (нужно определить)
            # Улучшения: каждый уровень на 50% дольше предыдущего
            # Уровень 1: 1 день, Уровень 2: 1 * 1.5 = 1.5 дня и т.д.
            "upgrade_times": [] # Будет рассчитано по формуле
        },
        "effects": {
            "research_speed_bonus": {
                # Совокупный бонус до 30%
                # Уровни 1-4: +1% каждый (4%)
                # Уровни 5-8: +1.5% каждый (6%)
                # Уровни 9-12: +2% каждый (8%)
                # Уровни 13-14: +3.5% каждый (7%)
                # Уровень 15: +5% (5%)
                # Итого: 30%
                "per_level": [
                    1, 1, 1, 1,      # Уровни 1-4
                    1.5, 1.5, 1.5, 1.5,  # Уровни 5-8
                    2, 2, 2, 2,      # Уровни 9-12
                    3.5, 3.5,        # Уровни 13-14
                    5               # Уровень 15
                ]
            }
        }
    }
}

# Дополнительная обработка для сложных формул стоимости
# Генератор AOM - улучшения
aom_upgrade_times = [1.0] # Уровень 1 (улучшение после постройки)
for i in range(2, 21): # Уровни 2-20
    aom_upgrade_times.append(aom_upgrade_times[-1] * 1.2)
    
BUILDINGS_DATA["aom_generator"]["costs"]["upgrade_times"] = aom_upgrade_times[1:] # Без базового уровня

# Арканская лаборатория - улучшения
arcane_upgrade_times = [1.0] # Уровень 1
for i in range(2, 16): # Уровни 2-15
    arcane_upgrade_times.append(arcane_upgrade_times[-1] * 1.5)
    
BUILDINGS_DATA["arcane_lab"]["costs"]["upgrade_times"] = arcane_upgrade_times[1:] # Без базового уровня

# Функция для получения данных о здании
def get_building_data(building_id):
    """Получить конфигурацию здания по его ID."""
    return BUILDINGS_DATA.get(building_id)

# Функция для получения времени постройки/улучшения
def get_building_time(building_id, level=None):
    """
    Получить время постройки или улучшения здания.
    ВСЕГДА возвращает 0 секунд для мгновенного строительства.
    
    Args:
        building_id (str): ID здания.
        level (int, optional): Уровень для улучшения. 
        
    Returns:
        float: Время в секундах (всегда 0).
    """
    # Игнорируем building_id и level, возвращаем 0 секунд для мгновенного завершения
    return 0.0 # 0 секунд

# Функция для получения максимального уровня здания
def get_max_level(building_id):
    """Получить максимальный уровень здания."""
    building = get_building_data(building_id)
    return building["max_level"] if building else 0
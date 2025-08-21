# spells_config.py
"""Конфигурация заклинаний для Academy of Elements."""

# --- Базовые параметры ---
# Базовый урон заклинания 1 уровня
BASE_SPELL_DAMAGE = 20
# Бонус урона за уровень (в процентах)
DAMAGE_PER_LEVEL_PERCENT = 20

# --- Данные о школах магии ---
SCHOOLS_DATA = {
    "fire": {
        "name": "Огонь",
        "name_rus": "Огня",  # Для сообщений типа "заклинание школы Огня"
        "color": "red", # Для веб-интерфейса
        "emoji": "🔥"
    },
    "water": {
        "name": "Вода",
        "name_rus": "Воды",
        "color": "blue",
        "emoji": "💧"
    },
    "wind": {
        "name": "Ветер",
        "name_rus": "Ветра",
        "color": "gray",
        "emoji": "🌪️"
    },
    "earth": {
        "name": "Земля",
        "name_rus": "Земли",
        "color": "brown",
        "emoji": "🌿"
    }
}

# --- Данные о заклинаниях ---
# Структура: школа -> ступень -> данные заклинания
SPELLS_DATA = {
    "fire": {
        1: {
            "id": "spark",
            "name": "Искра",
            "description": "Создаёт небольшую вспышку огня, наносящую урон одной цели.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {} # Эффекты на уровнях 1-4 (если нужны)
        },
        2: {
            "id": "firebolt",
            "name": "Огненная стрела",
            "description": "Бросает во врага стрелу пламени, пробивая его защиту.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        3: {
            "id": "fireball",
            "name": "Огненный шар",
            "description": "Создаёт взрывающийся шар огня, наносящий урон по области.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        4: {
            "id": "inferno",
            "name": "Инферно",
            "description": "Вызывает поток огня, опаляющий врагов в широком радиусе.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        5: {
            "id": "meteor",
            "name": "Метеорит",
            "description": "Призывает огненный метеорит с неба, наносящий огромный урон.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {
                "burn": "Накладывает эффект горения на 3 хода, наносящий урон каждый ход."
            }
        }
    },
    "water": {
        1: {
            "id": "icicle",
            "name": "Ледышка",
            "description": "Создаёт острый ледяной кристалл, поражающий цель.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        2: {
            "id": "frost_arrow",
            "name": "Ледяная стрела",
            "description": "Выпускает стрелу льда, замедляющую цель при попадании.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        3: {
            "id": "ice_shard",
            "name": "Ледяной осколок",
            "description": "Разбрасывает острые ледяные осколки вокруг, поражая несколько целей.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        4: {
            "id": "blizzard",
            "name": "Метель",
            "description": "Создаёт бурю из льда и снега, наносящую урон и снижающую меткость врагов.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        5: {
            "id": "tsunami",
            "name": "Цунами",
            "description": "Вызывает мощную волну, сметающую всех врагов на своём пути.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {
                "slow": "Замедляет цель на 2 хода, снижая её скорость атаки."
            }
        }
    },
    "wind": {
        1: {
            "id": "gust",
            "name": "Порыв",
            "description": "Создаёт резкий порыв ветра, отбрасывающий цель назад.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        2: {
            "id": "wind_blade",
            "name": "Ветрорез",
            "description": "Сформировывает острый клинок из воздуха, разящий цель.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        3: {
            "id": "cyclone",
            "name": "Циклон",
            "description": "Поднимает врага в воздух, лишая возможности атаковать на следующий ход.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        4: {
            "id": "lightning",
            "name": "Молния",
            "description": "Поражает цель разрядом молнии, обладающим высокой проникающей способностью.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        5: {
            "id": "tornado",
            "name": "Торнадо",
            "description": "Создаёт мощный вихрь, высасывающий жизнь из врагов.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {
                "stun": "Оглушает цель на 1 ход, полностью лишая возможности действовать."
            }
        }
    },
    "earth": {
        1: {
            "id": "pebble",
            "name": "Камешек",
            "description": "Бросает острый камень во врага, нанося ему урон.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        2: {
            "id": "stone_spike",
            "name": "Каменный шип",
            "description": "Из земли вырастает острый шип, пронзающий цель.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        3: {
            "id": "boulder",
            "name": "Валун",
            "description": "Швыряет огромный валун, наносящий урон и оглушающий при ударе.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        4: {
            "id": "earth_spike",
            "name": "Земляной пик",
            "description": "Поднимает из земли ряд острых пиков, поражая группу врагов.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {}
        },
        5: {
            "id": "earthquake",
            "name": "Землетрясение",
            "description": "Создаёт мощное землетрясение, обрушивающее стены и наносящее урон всем врагам.",
            "base_damage": BASE_SPELL_DAMAGE,
            "effects": {
                "defense_down": "Снижает защиту всех врагов на 20% на 2 хода."
            }
        }
    }
}

# --- Данные о гибридных заклинаниях ---
# Ключ - frozenset из двух ID школ (для уникальности, независимо от порядка)
# Значение - данные гибридного заклинания
HYBRID_SPELLS_DATA = {
    frozenset(["fire", "water"]): {
        "id": "steam",
        "name": "Пар",
        "description": "Создаёт обжигающий пар, наносящий урон по области и снижающий точность целей.",
        "base_damage": BASE_SPELL_DAMAGE,
        "effects": {
            "level_5": "Наносит урон по области и снижает точность цели на 15% на 2 хода."
        }
    },
    frozenset(["fire", "wind"]): {
        "id": "firestorm",
        "name": "Огненный вихрь",
        "description": "Создаёт вихрь пламени, опаляющий врагов и отбрасывающий их назад.",
        "base_damage": BASE_SPELL_DAMAGE,
        "effects": {
            "level_5": "Наносит урон по области и отбрасывает цель назад на 1 клетку."
        }
    },
    frozenset(["fire", "earth"]): {
        "id": "magma",
        "name": "Магма",
        "description": "Извергает раскалённую магму, наносящую урон и поджигающую землю.",
        "base_damage": BASE_SPELL_DAMAGE,
        "effects": {
            "level_5": "Наносит урон и накладывает эффект 'горение' на 4 хода."
        }
    },
    frozenset(["water", "wind"]): {
        "id": "ice_storm",
        "name": "Ледяной шторм",
        "description": "Вызывает шторм из ледяных осколков, наносящий урон и имеющий шанс заморозить цель.",
        "base_damage": BASE_SPELL_DAMAGE,
        "effects": {
            "level_5": "Наносит урон по области и замораживает цель на 1 ход (20% шанс)."
        }
    },
    frozenset(["water", "earth"]): {
        "id": "geyser",
        "name": "Гейзер",
        "description": "Поднимает струю кипящей воды из земли, наносящую урон и исцеляющую заклинателя.",
        "base_damage": BASE_SPELL_DAMAGE,
        "effects": {
            "level_5": "Наносит урон и лечит заклинателя на 30% от нанесённого урона."
        }
    },
    frozenset(["wind", "earth"]): {
        "id": "dust_devil",
        "name": "Пыльный вихрь",
        "description": "Создаёт вихрь из камней и пыли, ослепляющий и ранящий врагов.",
        "base_damage": BASE_SPELL_DAMAGE,
        "effects": {
            "level_5": "Наносит урон и ослепляет цель на 2 хода (снижает урон на 25%)."
        }
    }
    # ... (остальные 24 комбинации можно добавить аналогично)
}

# --- Вспомогательные функции ---

def get_spell_info(faction, tier):
    """Получить информацию о заклинании по школе и ступени."""
    return SPELLS_DATA.get(faction, {}).get(tier, {})

def get_hybrid_spell_info(schools_pair):
    """Получить информацию о гибридном заклинании по паре школ."""
    # frozenset делает порядок школ незначимым
    return HYBRID_SPELLS_DATA.get(frozenset(schools_pair), {})

def calculate_damage(base_damage, level):
    """Рассчитывает урон заклинания на заданном уровне."""
    if level < 1:
        return 0
    # Урон = Базовый * (1 + (Уровень - 1) * Бонус за уровень)
    return base_damage * (1 + (level - 1) * DAMAGE_PER_LEVEL_PERCENT / 100)

# ... другие вспомогательные функции
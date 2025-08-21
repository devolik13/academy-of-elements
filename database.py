# database.py
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

# Импортируем конфигурацию зданий
from buildings_config import BUILDINGS_DATA

load_dotenv()

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")

if not FIREBASE_CREDENTIALS_PATH:
    raise Exception("❌ FIREBASE_CREDENTIALS_PATH не найден в .env")

# Инициализация Firebase Admin SDK
try:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://academy-of-elements-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    print("✅ Подключение к Firebase инициализировано")
except Exception as e:
    raise Exception(f"❌ Ошибка инициализации Firebase: {e}")

# Функции для работы с пользователями
class UserDatabase:
    @staticmethod
    async def get_user(user_id):
        """Получить пользователя по ID"""
        try:
            ref = db.reference(f'users/{user_id}')
            user_data = ref.get()
            return user_data
        except Exception as e:
            print(f"❌ Ошибка при получении пользователя: {e}")
            return None

    @staticmethod
    async def create_user(user_id, username, faction):
        """Создать нового пользователя с начальными данными"""
        try:
            ref = db.reference(f'users/{user_id}')
            
            # Определяем начальное заклинание в зависимости от фракции
            initial_spell_data = {
                "fire": {"id": "spark", "name": "Искра"},
                "water": {"id": "icicle", "name": "Ледышка"},
                "wind": {"id": "gust", "name": "Порыв"},
                "earth": {"id": "pebble", "name": "Камешек"}
            }.get(faction, {"id": "spark", "name": "Искра"})
            
            initial_spell_id = initial_spell_data["id"]
            initial_spell_name = initial_spell_data["name"]

            # Инициализируем пустую сетку зданий (3x3 = 9 ячеек)
            buildings_grid = [None] * 9  # None означает пустую ячейку
            
            # Определяем стартовые здания
            starting_buildings = {}
            
            # Библиотека (id: "library") - стартовое здание в центре (ячейка 4)
            library_index = 4
            buildings_grid[library_index] = "library"
            starting_buildings["library"] = {
                "level": 1,
                "cell_index": library_index,
                "building_id": "library"
            }
            
            # Башня магов (id: "wizard_tower") - стартовое здание (например, в ячейке 25)
            wizard_tower_index = 6
            buildings_grid[wizard_tower_index] = "wizard_tower"
            starting_buildings["wizard_tower"] = {
                "level": 1,
                "cell_index": wizard_tower_index,
                "building_id": "wizard_tower"
            }

            user_data = {
                'username': username,
                'faction': faction,
                'last_energy_reset': None,
                'created_at': {".sv": "timestamp"}, # Серверное время Firebase
                
                # --- СИСТЕМА ЗДАНИЙ ---
                # Сетка городских зданий (3x3)
                'buildings_grid': buildings_grid,
                
                # Информация о построенных зданиях и их уровнях
                'buildings': starting_buildings,
                
                # Активная постройка/улучшение
                'construction': {
                    "active": False,
                    "building_id": None,
                    "target_level": None,
                    "time_left": 0,
                    "cell_index": None,
                    "type": None # "build" или "upgrade"
                },
                
                # --- СИСТЕМА АРМИИ ---
                'spells': {
                    "fire": {},
                    "water": {},
                    "wind": {},
                    "earth": {}
                },
                'research': {
                    "active": False,
                    "spell": None,
                    "target_level": None,
                    "time_left": 0,
                    "faction_bonus": False
                },
                'wizards': [
                    {
                        "id": "wizard_1",
                        "name": "Начальный маг",
                        "faction": faction,
                        "spells": [initial_spell_id]
                    }
                ],
                'available_spells': [initial_spell_id]
            }
            
            # Инициализируем начальное заклинание для фракции пользователя
            user_data['spells'][faction] = {
                initial_spell_id: {
                    "name": initial_spell_name,
                    "level": 1,
                    "tier": 1
                }
            }
            
            ref.set(user_data)
            return user_data
        except Exception as e:
            print(f"❌ Ошибка при создании пользователя: {e}")
            return None

    @staticmethod
    async def update_user(user_id, data):
        """Обновить данные пользователя"""
        try:
            ref = db.reference(f'users/{user_id}')
            ref.update(data)
            return True
        except Exception as e:
            print(f"❌ Ошибка при обновлении пользователя: {e}")
            return False

    @staticmethod
    async def add_spell_to_user(user_id, faction, spell_id, spell_data):
        """Добавить новое заклинание пользователю"""
        try:
            ref = db.reference(f'users/{user_id}/spells/{faction}/{spell_id}')
            ref.set(spell_data)
            return True
        except Exception as e:
            print(f"❌ Ошибка при добавлении заклинания: {e}")
            return False

    @staticmethod
    async def update_research(user_id, research_data):
        """Обновить данные о текущем исследовании"""
        try:
            ref = db.reference(f'users/{user_id}/research')
            ref.update(research_data)
            return True
        except Exception as e:
            print(f"❌ Ошибка при обновлении исследования: {e}")
            return False

    @staticmethod
    async def add_wizard(user_id, wizard_data):
        """Добавить нового мага пользователю"""
        try:
            ref = db.reference(f'users/{user_id}/wizards')
            wizards_snapshot = ref.get()
            wizards_list = wizards_snapshot if isinstance(wizards_snapshot, list) else []
            wizards_list.append(wizard_data)
            ref.set(wizards_list)
            return True
        except Exception as e:
            print(f"❌ Ошибка при добавлении мага: {e}")
            return False

    @staticmethod
    async def add_available_spell(user_id, spell_id):
        """Добавить заклинание в список доступных"""
        try:
            ref = db.reference(f'users/{user_id}/available_spells')
            spells_snapshot = ref.get()
            spells_list = spells_snapshot if isinstance(spells_snapshot, list) else []
            if spell_id not in spells_list:
                spells_list.append(spell_id)
                ref.set(spells_list)
            return True
        except Exception as e:
            print(f"❌ Ошибка при добавлении доступного заклинания: {e}")
            return False

    @staticmethod
    async def update_spell(user_id, faction, spell_id, spell_updates):
        """Обновить информацию о конкретном заклинании"""
        try:
            ref = db.reference(f'users/{user_id}/spells/{faction}/{spell_id}')
            ref.update(spell_updates)
            return True
        except Exception as e:
            print(f"❌ Ошибка при обновлении заклинания: {e}")
            return False
            
    @staticmethod
    async def update_building(user_id, building_id, building_updates):
        """Обновить информацию о конкретном здании"""
        try:
            ref = db.reference(f'users/{user_id}/buildings/{building_id}')
            ref.update(building_updates)
            return True
        except Exception as e:
            print(f"❌ Ошибка при обновлении здания: {e}")
            return False
            
    @staticmethod
    async def set_building_in_grid(user_id, cell_index, building_id):
        """Поставить или удалить здание в сетке"""
        try:
            ref = db.reference(f'users/{user_id}/buildings_grid/{cell_index}')
            ref.set(building_id) # building_id или None для удаления
            return True
        except Exception as e:
            print(f"❌ Ошибка при обновлении сетки зданий: {e}")
            return False
            
    @staticmethod
    async def start_construction(user_id, construction_data):
        """Начать постройку или улучшение здания"""
        try:
            ref = db.reference(f'users/{user_id}/construction')
            ref.set(construction_data)
            return True
        except Exception as e:
            print(f"❌ Ошибка при начале строительства: {e}")
            return False
            
    @staticmethod
    async def finish_construction(user_id, building_id, target_level, cell_index=None):
        """Завершить постройку или улучшение здания"""
        try:
            # Обновляем информацию о здании
            building_ref = db.reference(f'users/{user_id}/buildings/{building_id}')
            building_data = building_ref.get() or {}
            
            # Обновляем уровень здания
            building_data.update({
                "level": target_level,
                "building_id": building_id
            })
            
            if cell_index is not None:
                building_data["cell_index"] = cell_index
                
            building_ref.set(building_data)
            
            # Если это новое здание, обновляем сетку
            if cell_index is not None:
                grid_ref = db.reference(f'users/{user_id}/buildings_grid/{cell_index}')
                grid_ref.set(building_id)
            
            # Очищаем данные о строительстве
            construction_ref = db.reference(f'users/{user_id}/construction')
            construction_ref.set({
                "active": False,
                "building_id": None,
                "target_level": None,
                "time_left": 0,
                "cell_index": None,
                "type": None
            })
            
            return True
        except Exception as e:
            print(f"❌ Ошибка при завершении строительства: {e}")
            return False
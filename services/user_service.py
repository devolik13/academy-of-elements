from database import UserDatabase

class UserService:
    @staticmethod
    async def create_new_user(user_id, username, faction):
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

            # Инициализируем пустую сетку зданий (7x7 = 49 ячеек)
            buildings_grid = [None] * 49  # None означает пустую ячейку
            
            # Определяем стартовые здания
            starting_buildings = {}
            
            # Библиотека (id: "library") - стартовое здание в центре (ячейка 24)
            library_index = 24
            buildings_grid[library_index] = "library"
            starting_buildings["library"] = {
                "level": 1,
                "cell_index": library_index,
                "building_id": "library"
            }
            
            # Башня магов (id: "wizard_tower") - стартовое здание (например, в ячейке 25)
            wizard_tower_index = 25
            buildings_grid[wizard_tower_index] = "wizard_tower"
            starting_buildings["wizard_tower"] = {
                "level": 1,
                "cell_index": wizard_tower_index,
                "building_id": "wizard_tower"
            }

            user_data = {
                'username': username,
                'faction': faction,
                'mana': 100,
                'crystals': 50,
                'energy': 3,
                'last_energy_reset': None,
                'created_at': {".sv": "timestamp"}, # Серверное время Firebase
                
                # --- СИСТЕМА ЗДАНИЙ ---
                # Сетка городских зданий (7x7)
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